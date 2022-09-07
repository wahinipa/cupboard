#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.commons.base_models import BaseModel


class Role(BaseModel):
    assignments = database.relationship('Assignment', backref='role', lazy=True, cascade='all, delete')


class Assignment(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    group_id = database.Column(database.Integer, database.ForeignKey('group.id'))
    role_id = database.Column(database.Integer, database.ForeignKey('role.id'))
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    date_created = database.Column(database.DateTime(), default=datetime.now())


def create_role(name, description="", date_created=None):
    if date_created is None:
        date_created = datetime.now()
    role = Role(name=name, description=description, date_created=date_created)
    database.session.add(role)
    database.session.commit()
    return role


def assign_role(group, role, user, date_created=None):
    if date_created is None:
        date_created = datetime.now()
    assignment = Assignment(group=group, role=role, person=user, date_created=date_created)
    database.session.add(assignment)
    database.session.commit()
    return assignment
