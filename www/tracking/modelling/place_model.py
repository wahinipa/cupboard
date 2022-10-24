#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from sqlalchemy.orm import backref

from tracking import database
from tracking.modelling.base_models import NamedBaseModel, RootDescendantMixin
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


class Place(RootDescendantMixin, CupboardDisplayContextMixin, NamedBaseModel):
    singular_label = "Place"
    plural_label = "Places"
    possible_tasks = ['create', 'update', 'delete']
    label_prefixes = {'create': 'Place for '}
    flavor = "place"

    roots = database.relationship('Root', backref='place', lazy=True)

    place_id = database.Column(database.Integer, database.ForeignKey('place.id'), index=True)
    places = database.relationship('Place', lazy='subquery', backref=backref('place_of', remote_side='Place.id'))
    positionings = database.relationship('Positioning', backref='place', lazy=True, cascade='all, delete')
    assignments = database.relationship('PlaceAssignment', backref='place', lazy=True, cascade='all, delete')

    def has_role(self, person, name_of_role):
        def yes(assignment):
            return assignment.person == person and assignment.role.is_named(name_of_role)

        return any(map(yes, self.assignments)) or self.ancestor.has_role(person, name_of_role)

    @property
    def identities(self):
        return {'place_id': self.id}

    @property
    def children(self):
        return self.places

    @property
    def domain(self):
        result = []
        for place in self.places:
            result += place.complete_domain
        return result

    @property
    def complete_domain(self):
        return self.domain + [self]

    def add_to_thing(self, particular_thing, quantity):
        from tracking.modelling.postioning_model import add_quantity_of_things
        return add_quantity_of_things(self, particular_thing, quantity)

    def quantity_of_things(self, thing):
        from tracking.modelling.postioning_model import find_exact_quantity_of_things_at_place
        return find_exact_quantity_of_things_at_place(self, thing)

    def create_kind_of_place(self, name, description, date_created=None):
        if date_created is None:
            date_created = datetime.now()
        place = Place(name=name, description=description, place_of=self, date_created=date_created)
        database.session.add(place)
        database.session.commit()
        return place

    def may_perform_task(self, viewer, task):
        if task == 'view':
            return self.may_be_observed(viewer)
        elif task == 'create':
            return self.may_create_place(viewer)
        elif task == 'delete':
            return self.may_delete(viewer) and not self.is_top
        elif task == 'update':
            return self.may_update(viewer) and not self.is_top
        else:
            return False

    def may_be_observed(self, viewer):
        return self.ancestor.may_be_observed(viewer)

    def may_create_place(self, viewer):
        return self.ancestor.may_create_place(viewer)

    def may_delete(self, viewer):
        return self.ancestor.may_delete(viewer)

    def may_update(self, viewer):
        return self.ancestor.may_update(viewer)

    @property
    def page_template(self):
        return "pages/place_view.j2"

    @property
    def parent_object(self):
        return self.place_of

    @property
    def root(self):
        from tracking.modelling.root_model import place_root
        return place_root(self)

    @property
    def top_thing(self):
        return self.root.thing

    def viewable_children(self, viewer):
        return self.sorted_children


def find_place_by_id(place_id):
    return Place.query.filter(Place.id == place_id).first()
