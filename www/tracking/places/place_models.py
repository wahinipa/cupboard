# Copyright 2022 Wahinipa LLC
from datetime import datetime

from tracking import database


class Place(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    group_id = database.Column(database.Integer, database.ForeignKey('group.id'))
    name = database.Column(database.String(255), nullable=False, unique=True)
    description = database.Column(database.Text(), nullable=False, server_default='')
    date_created = database.Column(database.DateTime(), default=datetime.now())
