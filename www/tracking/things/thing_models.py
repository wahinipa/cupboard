# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for
from sqlalchemy.orm import backref

from tracking import database
from tracking.commons.base_models import IdModelMixin, UniqueNamedBaseModel, name_is_key


class Thing(UniqueNamedBaseModel):
    kind_of_id = database.Column(database.Integer, database.ForeignKey('thing.id'), index=True)

    kinds = database.relationship('Thing', backref=backref('kind_of', remote_side='Thing.id'))
    refinements = database.relationship('Refinement', backref='thing', lazy=True, cascade='all, delete')
    particular_things = database.relationship('ParticularThing', backref='thing', lazy=True, cascade='all, delete')

    @property
    def sorted_kinds(self):
        return sorted(self.kinds, key=name_is_key)

    @property
    def url(self):
        return url_for('thing_bp.thing_view', thing_id=self.id)

    def quantity_at_place(self, place):
        return sum(particular_thing.quantity_at_place(place) for particular_thing in self.particular_things) + sum(
            thing.quantity_at_place(place) for thing in self.kinds
        )

    @property
    def generic(self):
        return find_or_create_particular_thing(self, [])


    def viewable_attributes(self, viewer, include_actions=False):
        attributes = {
            'name': self.name,
            'url': self.url,
            'lines': self.description_lines,
            'kinds': [thing.viewable_attributes(viewer) for thing in self.sorted_kinds]
        }
        if include_actions:
            if viewer.may_delete_group:
                attributes['deletion_url'] = self.deletion_url
            if viewer.may_update_group:
                attributes['update_url'] = self.update_url
            if self.user_may_create_place(viewer):
                attributes['create_place_url'] = self.place_create_url
        return attributes

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
