# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database


class Thing(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False, unique=True)
    description = database.Column(database.Text(), nullable=False, server_default='')
    date_created = database.Column(database.DateTime(), default=datetime.now())


def create_thing(name, description, date_created=None):
    if date_created is None:
        date_created = datetime.now()
    thing = Thing(name=name, description=description, date_created=date_created)
    database.session.add(thing)
    database.session.commit()
    return thing
