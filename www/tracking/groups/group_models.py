# Copyright 2022 Wahinipa LLC
from datetime import datetime

from tracking import database


class Group(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False, unique=True)
    description = database.Column(database.Text(), nullable=False, server_default='')
    date_created = database.Column(database.DateTime(), default=datetime.now())

    # roles = database.relationship('Role', backref='group', lazy=True, cascade='all, delete')
    # places = database.relationship('Place', backref='group', lazy=True, cascade='all, delete')