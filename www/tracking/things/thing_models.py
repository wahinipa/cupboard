# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database


class Thing(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False, unique=True)
    description = database.Column(database.Text(), nullable=False, server_default='')
    date_created = database.Column(database.DateTime(), default=datetime.now())


def find_or_create_thing(name, description, date_created=None):
    thing = find_thing_by_name(name)
    if thing is None:
        if date_created is None:
            date_created = datetime.now()
        thing = Thing(name=name, description=description, date_created=date_created)
        database.session.add(thing)
        database.session.commit()
    return thing


def find_thing_by_name(name):
    return Thing.query.filter(Thing.name == name).first()
