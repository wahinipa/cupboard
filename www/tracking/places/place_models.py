# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.commons.base_models import BaseModel


class Place(BaseModel):
    group_id = database.Column(database.Integer, database.ForeignKey('group.id'))
    place_assignments = database.relationship('PlaceAssignment', backref='place', lazy=True, cascade='all, delete')
    positionings = database.relationship('Positioning', backref='place', lazy=True, cascade='all, delete')

    def quantity_of_things(self, thing):
        from tracking.positionings.postioning_models import find_quantity_of_things
        return find_quantity_of_things(self, thing)

    def add_to_thing(self, particular_thing, quantity):
        from tracking.positionings.postioning_models import add_quantity_of_things
        return add_quantity_of_things(self, particular_thing, quantity)

    def has_role(self, person, name_of_role):
        for assignment in self.place_assignments:
            if assignment.person == person and assignment.role.name == name_of_role:
                return True
        return self.group.has_role(person, name_of_role)


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
