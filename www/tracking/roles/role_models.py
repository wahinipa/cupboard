#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database


class Role(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False, unique=True)
    description = database.Column(database.Text(), nullable=False, server_default='')
    date_created = database.Column(database.DateTime(), default=datetime.now())

    assignments = database.relationship('Assignment', backref='role', lazy=True, cascade='all, delete')


class Assignment(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    role_id = database.Column(database.Integer, database.ForeignKey('role.id'))
    group_id = database.Column(database.Integer, database.ForeignKey('group.id'))
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
