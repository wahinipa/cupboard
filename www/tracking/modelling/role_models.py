#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from sqlalchemy.orm import declared_attr

from tracking import database
from tracking.modelling.base_models import UniqueNamedBaseModel, IdModelMixin, DatedModelMixin

class Role(UniqueNamedBaseModel):
    root_assignments = database.relationship('RootAssignment', backref='role', lazy=True, cascade='all, delete')
    place_assignments = database.relationship('PlaceAssignment', backref='role', lazy=True, cascade='all, delete')
    universal_assignments = database.relationship('UniversalAssignment', backref='role', lazy=True,
                                                  cascade='all, delete')

    observer_role = "Observer"
    create_user_role = "Create User"
    delete_user_role = "Delete User"

    @property
    def is_observer_role(self):
        return self.is_named(self.observer_role)

    def is_named(self, name_of_role):
        return self.name == name_of_role


def find_role_by_id(id):
    return Role.query.filter(Role.id == id).first()


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


def find_or_create_standard_roles():
    return [
        find_or_create_role(Role.create_user_role, "Can create new user account (i.e. login)."),
        find_or_create_role(Role.delete_user_role, "Can delete current user account."),
        find_or_create_role(Role.observer_role, "Can view, search, and generate reports."),
    ]

class KnowsOwnName:
    def is_named(self, name):
        return self.name == name


class AssignmentBaseModel(IdModelMixin, DatedModelMixin, KnowsOwnName, database.Model):
    __abstract__ = True

    @declared_attr
    def role_id(cls):
        return database.Column(database.Integer, database.ForeignKey('role.id'))

    @declared_attr
    def user_id(cls):
        return database.Column(database.Integer, database.ForeignKey('user.id'))

    @property
    def is_observer(self):
        return self.role.is_observer_role

    @property
    def name(self):
        return self.role.name


class RootAssignment(AssignmentBaseModel):
    root_id = database.Column(database.Integer, database.ForeignKey('root.id'))


class PlaceAssignment(AssignmentBaseModel):
    place_id = database.Column(database.Integer, database.ForeignKey('place.id'))


class UniversalAssignment(AssignmentBaseModel):
    pass


def find_root_assignment(root, role, user):
    for root_assignment in user.root_assignments:
        if root_assignment.root == root and root_assignment.role == role:
            return root_assignment
    return None


def find_place_assignment(place, role, user):
    for place_assignment in user.place_assignments:
        if place_assignment.place == place and place_assignment.role == role:
            return place_assignment
    return None


def find_universal_assignment(role, user):
    for universal_assignment in user.universal_assignments:
        if universal_assignment.role == role:
            return universal_assignment
    return None


def assign_root_role(root, role, user, date_created=None):
    assignment = find_root_assignment(root, role, user)
    if assignment is None:
        if date_created is None:
            date_created = datetime.now()
        assignment = RootAssignment(root=root, role=role, person=user, date_created=date_created)
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


def assign_universal_role(role, user, date_created=None):
    assignment = find_universal_assignment(role, user)
    if assignment is None:
        if date_created is None:
            date_created = datetime.now()
        assignment = UniversalAssignment(role=role, person=user, date_created=date_created)
        database.session.add(assignment)
        database.session.commit()
    return assignment
