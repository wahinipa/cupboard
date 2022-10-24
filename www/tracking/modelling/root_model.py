#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.modelling.base_models import UniqueNamedBaseModel
from tracking.modelling.cardistry_models import name_is_key, sorted_by_name
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


class Root(CupboardDisplayContextMixin, UniqueNamedBaseModel):
    singular_label = "Organizational Association"
    plural_label = "Organizational Associations"
    possible_tasks = ['update', 'delete']
    label_prefixes = {}
    flavor = "root"

    place_id = database.Column(database.Integer, database.ForeignKey('place.id'), unique=True, nullable=False)
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'), unique=True, nullable=False)

    categories = database.relationship('Category', backref='root', lazy=True, cascade='all, delete')
    assignments = database.relationship('RootAssignment', backref='root', lazy=True, cascade='all, delete')
    specifications = database.relationship('Specification', backref='root', lazy=True, cascade='all, delete')

    def has_role(self, person, name_of_role):
        def yes(assignment):
            return assignment.person == person and assignment.role.is_named(name_of_role)

        return any(map(yes, self.assignments))

    @property
    def identities(self):
        return {'root_id': self.id}

    @property
    def generic_specification(self):
        return self.find_or_create_specification()

    @property
    def sorted_categories(self):
        return sorted_by_name(self.categories)

    def create_category(self, name, description, date_created=None):
        from tracking.modelling.category_model import Category
        if date_created is None:
            date_created = datetime.now()
        category = Category(name=name, description=description, root=self, date_created=date_created)
        database.session.add(category)
        database.session.commit()
        return category

    def find_or_create_specification(self, choices=None, date_created=None, commit=True):
        from tracking.modelling.specification_model import Specification
        from tracking.modelling.specification_model import Specific
        if choices is None:
            choices = set()
        else:
            choices = set(choices)  # Allow any iterable
        if date_created is None:
            date_created = datetime.now()
        specification = self.find_specification(choices)
        if specification is None:
            specification = Specification(root=self, date_created=date_created)
            for choice in choices:
                specific = Specific(choice=choice, specification=specification)
                database.session.add(specific)
            database.session.add(specification)
            if commit:
                database.session.commit()
        return specification

    def find_specification(self, choices=None):
        if choices is None:
            choices = set()
        else:
            choices = set(choices)  # Allow any iterable
        for specification in self.specifications:
            if choices == specification.choices:
                return specification
        return None




    def may_perform_task(self, viewer, task):
        if task == 'view':
            return self.may_be_observed(viewer)
        elif task == 'delete':
            return self.may_delete(viewer)
        elif task == 'update':
            return self.may_update(viewer)
        elif task == 'create_place':
            return self.may_create_place(viewer)
        elif task == 'create_thing':
            return self.may_create_thing(viewer)
        else:
            return False

    def may_be_observed(self, viewer):
        return True

    def may_delete(self, viewer):
        return viewer.may_delete_root

    def may_create_place(self, viewer):
        return viewer.may_update_root

    def may_create_category(self, viewer):
        return viewer.may_update_root

    def may_create_thing(self, viewer):
        return viewer.may_update_root

    def may_update(self, viewer):
        return viewer.may_update_root

    @property
    def parent_object(self):
        return None

    def viewable_children(self, viewer):
        if self.may_be_observed(viewer):
            return [self.place, self.thing]
        else:
            return []


def all_roots():
    return sorted(Root.query.all(), key=name_is_key)


def create_root(name, description, date_created=None):
    if date_created is None:
        date_created = datetime.now()
    from tracking.modelling.place_model import Place
    place_name = f'Everywhere'
    place_description = f'All of the top places for {name}'
    place = Place(name=place_name, description=place_description, date_created=date_created)
    database.session.add(place)

    from tracking.modelling.thing_model import Thing
    thing_name = f'Everything'
    thing_description = f'All of the top things for {name}'
    thing = Thing(name=thing_name, description=thing_description, date_created=date_created)
    database.session.add(thing)

    root = Root(name=name, description=description, place=place, thing=thing, date_created=date_created)
    database.session.add(root)
    database.session.commit()

    return root


def find_root_by_id(root_id):
    return Root.query.filter(Root.id == root_id).first()


def place_root(place):
    top = place.top
    return Root.query.filter(Root.place_id == top.id).first()


def thing_root(thing):
    top = thing.top
    return Root.query.filter(Root.thing_id == top.id).first()
