# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ

from flask import url_for
from sqlalchemy.orm import backref

from tracking import database
from tracking.commons.base_models import IdModelMixin, UniqueNamedBaseModel, name_is_key
from tracking.commons.display_context import DisplayContext


class Thing(UniqueNamedBaseModel):
    kind_of_id = database.Column(database.Integer, database.ForeignKey('thing.id'), index=True)

    kinds = database.relationship('Thing', backref=backref('kind_of', remote_side='Thing.id'))
    refinements = database.relationship('Refinement', backref='thing', lazy=True, cascade='all, delete')
    particular_things = database.relationship('ParticularThing', backref='thing', lazy=True, cascade='all, delete')

    @property
    def label(self):
        if self.is_top:
            return "All Things"
        else:
            return self.name

    @property
    def is_top(self):
        return self.kind_of is None

    @property
    def parent_thing(self):
        root = self.kind_of
        if root and not root.is_top:
            return root
        else:
            return None

    @property
    def category_set(self):
        categories = {refinement.category for refinement in self.refinements}
        root = self.kind_of
        if root:
            categories |= root.category_set
        return categories

    @property
    def categories(self):
        return sorted(self.category_set, key=name_is_key)

    @property
    def sorted_kinds(self):
        return sorted(self.kinds, key=name_is_key)

    @property
    def url(self):
        if self.is_top:
            return url_for('thing_bp.thing_list')
        else:
            return url_for('thing_bp.thing_view', thing_id=self.id)

    @property
    def create_url(self):
        return url_for('thing_bp.thing_create', thing_id=self.id)

    @property
    def delete_url(self):
        return url_for('thing_bp.thing_delete', thing_id=self.id)

    @property
    def update_url(self):
        return url_for('thing_bp.thing_update', thing_id=self.id)

    @property
    def parent_list(self):
        parent = self.kind_of
        if parent is None:
            return []
        else:
            return parent.parent_list + [parent]

    def user_may_delete(self, user):
        return user.may_delete_thing and not self.is_top

    def user_may_update(self, user):
        return user.may_update_thing and not self.is_top

    def user_may_view(self, user):
        return user.may_observe_things

    def quantity_at_place(self, place):
        return sum(particular_thing.quantity_at_place(place) for particular_thing in self.particular_things) + sum(
            thing.quantity_at_place(place) for thing in self.kinds
        )

    @property
    def generic(self):
        return find_or_create_particular_thing(self, [])

    def viewable_nodes(self, viewer):
        return [thing.viewable_attributes(viewer) for thing in self.sorted_kinds]

    def viewable_attributes(self, viewer):
        description_nodes = [{'text': line} for line in self.description_lines]
        kind_of_nodes = self.viewable_nodes(viewer)  # No actions for lower nodes.
        link_nodes = [
            {
                'text': f'{self.label} Details',
                'url': self.url,
            }
        ]
        attributes = {
            'text': self.name,
            'nodes': description_nodes + link_nodes + kind_of_nodes,
        }
        return attributes


def thing_display_context(thing, viewer):
    thing_context = DisplayContext({
        'tab': 'thing',
        'label': thing.label,
        'parent_list': thing.parent_list,
        'nodes': thing.viewable_nodes(viewer),
        'categories': thing.categories,
    })
    if not thing.is_top:
        thing_context.add_attribute('lines', thing.description_lines)
    if viewer.may_create_thing:
        thing_context.add_action(thing.create_url, f'Kind of {thing.label}', 'create')
    if not thing.is_top:
        if viewer.may_update_thing:
            thing_context.add_action(thing.update_url, thing.label, 'update')
        if viewer.may_delete_thing:
            thing_context.add_action(thing.delete_url, thing.label, 'delete')
    return thing_context.display_context


def top_viewable_attributes(viewer):
    if viewer.may_observe:
        return find_or_create_everything().viewable_nodes(viewer)
    else:
        return []


def find_or_create_thing(name, description, kind_of=None, date_created=None):
    thing = find_thing_by_name(name)
    if thing is None:
        if kind_of is None:
            kind_of = find_or_create_everything()
        if date_created is None:
            date_created = datetime.now()
        thing = Thing(name=name, description=description, kind_of_id=kind_of.id, date_created=date_created)
        database.session.add(thing)
        database.session.commit()
    return thing


def find_thing_by_name(name):
    return Thing.query.filter(Thing.name == name).first()


def find_thing_by_id(id):
    return Thing.query.filter(Thing.id == id).first()


def find_or_create_everything():
    everything = find_thing_by_name("Everything")
    if everything is None:
        everything = Thing(name="Everything", description="All things")
        database.session.add(everything)
        database.session.commit()
    return everything


class Particular(IdModelMixin, database.Model):
    particular_thing_id = database.Column(database.Integer, database.ForeignKey('particular_thing.id'), index=True)
    choice_id = database.Column(database.Integer, database.ForeignKey('choice.id'), index=True)


def _find_or_create_particular(particular_thing, choice):
    particular = particular_thing.find_particular(choice)
    if particular is None:
        particular = Particular(particular_thing=particular_thing, choice=choice)
        database.session.add(particular)
        # Do not commit yet, else database could be corrupted by duplicates.
    return particular


class ParticularThing(IdModelMixin, database.Model):
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'), index=True)
    particulars = database.relationship('Particular', backref='particular_thing', lazy=True, cascade='all, delete')
    positionings = database.relationship('Positioning', backref='particular_thing', lazy=True, cascade='all, delete')

    @property
    def kind_of(self):
        return self.thing

    @property
    def choices(self):
        return [particular.choice for particular in self.particulars]

    def quantity_at_place(self, place):
        from tracking.positionings.postioning_models import find_quantity_of_things
        return find_quantity_of_things(place, self)

    def add_to_place(self, place, quantity):
        from tracking.positionings.postioning_models import add_quantity_of_things
        return add_quantity_of_things(place, self, quantity)

    def find_particular(self, choice):
        for particular in self.particulars:
            if particular.choice == choice:
                return particular
        return None


def find_or_create_particular_thing(thing, choices):
    particular_thing = find_particular_thing(thing, choices)
    if particular_thing is None:
        # Create ParticularThing...
        particular_thing = ParticularThing(thing=thing)
        database.session.add(particular_thing)
        for choice in choices:
            # ... and one Particular to capture each choice ...
            _find_or_create_particular(particular_thing, choice)
        # ... then commit the whole set into the database as a single transaction.
        database.session.commit()
    return particular_thing


def find_particular_thing(thing, choices):
    count = len(choices)

    def has_same_choices(particular_thing):
        possible_choices = particular_thing.choices
        if len(possible_choices) != count:
            return False
        else:
            for choice in choices:
                if choice not in possible_choices:
                    return False
            return True

    for particular_thing in thing.particular_things:
        if has_same_choices(particular_thing):
            return particular_thing
    return None


