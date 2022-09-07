# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database


class Place(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    group_id = database.Column(database.Integer, database.ForeignKey('group.id'))
    name = database.Column(database.String(255), nullable=False)
    description = database.Column(database.Text(), nullable=False, server_default='')
    date_created = database.Column(database.DateTime(), default=datetime.now())


def find_or_create_place(group, name, description, date_created=None):
    place = find_place(group, name)
    if place is None:
        if date_created is None:
            date_created = datetime.now()
        place = Place(group_id=group.id, name=name, description=description, date_created=date_created)
        database.session.add(place)
        database.session.commit()
    return place


def find_place(group, name):
    for place in group.places:
        if place.name == name:
            return place
    return None
