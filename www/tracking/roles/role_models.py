#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from sqlalchemy.orm import declared_attr

from tracking import database
from tracking.commons.base_models import DatedModelMixin, IdModelMixin, UniqueNamedBaseModel


class Role(UniqueNamedBaseModel):
    group_assignments = database.relationship('GroupAssignment', backref='role', lazy=True, cascade='all, delete')
    place_assignments = database.relationship('PlaceAssignment', backref='role', lazy=True, cascade='all, delete')
    universal_assignments = database.relationship('UniversalAssignment', backref='role', lazy=True,
                                                  cascade='all, delete')


class AssignmentBaseModel(IdModelMixin, DatedModelMixin, database.Model):
    __abstract__ = True

    @declared_attr
    def role_id(cls):
        return database.Column(database.Integer, database.ForeignKey('role.id'))

    @declared_attr
    def user_id(cls):
        return database.Column(database.Integer, database.ForeignKey('user.id'))


class GroupAssignment(AssignmentBaseModel):
    group_id = database.Column(database.Integer, database.ForeignKey('group.id'))


class PlaceAssignment(AssignmentBaseModel):
    place_id = database.Column(database.Integer, database.ForeignKey('place.id'))


class UniversalAssignment(AssignmentBaseModel):
    pass


def find_role(name):
    return Role.query.filter(Role.name == name).first()


def find_or_create_role(name, description="", date_created=None):
    role = find_role(name)
    if role is None:
        if date_created is None:
            date_created = datetime.now()
        role = Role(name=name, description=description, date_created=date_created)
        database.session.add(role)
        database.session.commit()
    return role


def find_group_assignment(group, role, user):
    for group_assignment in user.group_assignments:
        if group_assignment.group == group and group_assignment.role == role:
            return group_assignment
    return None


def find_place_assignment(place, role, user):
    for place_assignment in user.place_assignments:
        if place_assignment.place == place and place_assignment.role == role:
            return place_assignment
    return None


def assign_group_role(group, role, user, date_created=None):
    assignment = find_group_assignment(group, role, user)
    if assignment is None:
        if date_created is None:
            date_created = datetime.now()
        assignment = GroupAssignment(group=group, role=role, person=user, date_created=date_created)
        database.session.add(assignment)
        database.session.commit()
    return assignment


def assign_place_role(place, role, user, date_created=None):
    assignment = find_place_assignment(place, role, user)
    if assignment is None:
        if date_created is None:
            date_created = datetime.now()
        assignment = PlaceAssignment(place=place, role=role, person=user, date_created=date_created)
        database.session.add(assignment)
        database.session.commit()
    return assignment
