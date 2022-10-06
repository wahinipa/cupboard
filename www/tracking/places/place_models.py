# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for

from tracking import database
from tracking.commons.base_models import BaseModel, ModelWithRoles, name_is_key
from tracking.commons.display_context import DisplayContext
from tracking.commons.pseudo_model import PseudoModel


class AllPlaces(PseudoModel):
    def __init__(self, home):
        super().__init__(
            label="Places",
            endpoint='place_bp.place_list',
            description="Places are locations where Groups keep Things",
            parent_object=home
        )

    def may_be_observed(self, viewer):
        return viewer.may_observe_places

    @property
    def child_list(self):
        return sorted(Place.query.all(), key=name_is_key)



class Place(BaseModel, ModelWithRoles):
    group_id = database.Column(database.Integer, database.ForeignKey('group.id'))
    place_assignments = database.relationship('PlaceAssignment', backref='place', lazy=True, cascade='all, delete')
    positionings = database.relationship('Positioning', backref='place', lazy=True, cascade='all, delete')

    @property
    def assignments(self):
        return self.place_assignments + self.group.assignments

    def quantity_of_things(self, thing):
        from tracking.positionings.postioning_models import find_quantity_of_things
        return find_quantity_of_things(self, thing)

    def add_to_thing(self, particular_thing, quantity):
        from tracking.positionings.postioning_models import add_quantity_of_things
        return add_quantity_of_things(self, particular_thing, quantity)

    def user_may_update(self, user):
        return self.group.user_may_update(user)

    def may_be_observed(self, user):
        return self.group.may_be_observed(user)

    def viewable_attributes(self, viewer, include_group_url=True):
        group_notation = {
            'label': 'Group',
            'value': self.group.name,
        }
        if include_group_url:
            group_notation['url'] =  self.group.url
        notations = [group_notation] + self.description_notation
        attributes = {
            'classification': 'Place',
            'name': self.name,
            'label': self.label,
            'view_url': self.url,
            'notations': notations,
        }
        return attributes

    def display_context(self, viewer):
        place_context = DisplayContext({
            'target': self.viewable_attributes(viewer, include_group_url=True),
            'parent_list': self.parent_list,
            'label': self.label
        })
        if viewer.may_update_place:
            place_context.add_action(self.update_url, self.name, 'update')
        if viewer.may_delete_place:
            place_context.add_action(self.deletion_url, self.name, 'delete')
        return place_context

    @property
    def url(self):
        return url_for('place_bp.place_view', place_id=self.id)

    @property
    def deletion_url(self):
        return url_for('place_bp.place_delete', place_id=self.id)

    @property
    def update_url(self):
        return url_for('place_bp.place_update', place_id=self.id)

    @property
    def parent_list(self):
        return self.group.parent_list + [self.group]


def find_or_create_place(group, name, description, date_created=None):
    place = find_place(group, name)
    if place is None:
        if date_created is None:
            date_created = datetime.now()
        place = Place(group=group, name=name, description=description, date_created=date_created)
        database.session.add(place)
        database.session.commit()
    return place


def find_place(group, name):
    for place in group.places:
        if place.name == name:
            return place
    return None


def find_place_by_id(place_id):
    return Place.query.filter(Place.id == place_id).first()
