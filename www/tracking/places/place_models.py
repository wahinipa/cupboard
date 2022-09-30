# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ

from flask import url_for

from tracking import database
from tracking.commons.base_models import BaseModel, ModelWithRoles
from tracking.commons.display_context import DisplayContext


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

    def user_may_view(self, user):
        return self.group.user_may_view(user)

    def viewable_attributes(self, viewer, include_group_url=False):
        attributes = {
            'name': self.name,
            'url': self.url,
            'lines': self.description_lines,
            'group_name': self.group.name,
        }
        if include_group_url:
            attributes['group_url'] = self.group.url
        return attributes

    def display_context(self, viewer):
        place_context = DisplayContext({
            'place': self.viewable_attributes(viewer, include_group_url=True),
            'name': self.name,
            'group_url': self.group.url,
            'parent_list': self.parent_list,
            'label': self.label
        })
        if viewer.may_update_place:
            place_context.add_action(self.update_url, self.name, 'update')
        if viewer.may_delete_place:
            place_context.add_action(self.deletion_url, self.name, 'delete')
        return place_context.display_context

    @property
    def label(self):
        return self.name

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
        from tracking.groups.group_models import AllGroups
        return [AllGroups(), self.group]


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


def create_initial_places_and_groups():
    if environ.get('ADD_TEST_DATA'):
        from tracking.groups.group_models import find_or_create_group
        do_gooders = find_or_create_group("Do Gooders, Inc.", "Doing good\nwhile doing more good.")
        well_wishers = find_or_create_group("Society of Well Wishers",
                                            "If wishes were horses we would find you a pony.")
        find_or_create_place(do_gooders, "Out Back", "The shed behind the main office.\nClaudia has the key.")
        find_or_create_place(well_wishers, "Church Basement", "")
        find_or_create_place(well_wishers, "Main Storage Unit", "Unit 17 at Store-Your-Stuff-Here")
        find_or_create_place(well_wishers, "Garage", "Please keep locked when office is closed.")
