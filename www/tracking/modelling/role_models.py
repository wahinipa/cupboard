#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from sqlalchemy.orm import declared_attr

from tracking import database
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.base_models import DatedModelMixin, IdModelMixin, UniqueNamedBaseModel


class AllRoles:
    label = 'Roles'

    @property
    def identities(self):
        return {}

    @property
    def root_path(self):
        return [self]


class Role(CupboardDisplayContextMixin, UniqueNamedBaseModel):
    singular_label = "Role"
    plural_label = "Roles"
    possible_tasks = []
    label_prefixes = {}
    flavor = 'role'
    root_assignments = database.relationship('RootAssignment', backref='role', lazy=True, cascade='all, delete')
    place_assignments = database.relationship('PlaceAssignment', backref='role', lazy=True, cascade='all, delete')
    universal_assignments = database.relationship('UniversalAssignment', backref='role', lazy=True,
                                                  cascade='all, delete')

    user_admin_role_name = "User Account Manager"
    admin_role_name = "Organization Administrator"
    linkage_role_name = "Linking People"
    structuring_role_name = "Catalog Manager"
    structure_viewer_role_name = "Catalog Viewer"
    inventory_manager_name = "Inventory Manager"
    location_manager_name = "Location Manager"
    observer_role_name = "Observer"
    inbound_role_name = "Receiving Agent"
    outbound_role_name = "Shipping Agent"
    transfer_role_name = "Transfer Agent"
    adjust_role_name = "Auditing Agent"
    super_role_name = "Super Admin"  # No actual Role created for this
    self_role_name = "Viewer is Self"  # No actual Role created for this
    people_viewer_name = "Viewer of People"  # No actual Role created for this
    roots_observer_role_name = "Viewer of Roots"  # No actual Role created for this
    anybody_role_name = "Anybody"  # No actual Role created for this

    role_descriptions = {
        user_admin_role_name: "Can create, update, enable, disable, or delete user accounts.",
        admin_role_name: "Within an organization, can assign roles to people.",
        linkage_role_name: "Can associate user accounts with an organization.",
        structuring_role_name: "Within an organization, can update the catalog of things, categories, and choices.",
        structure_viewer_role_name: "Within an organization, can view the catalog of things, categories, and choices.",
        location_manager_name: "For a given location, can create, delete, or update sub-locations.",
        inventory_manager_name: "For a given location, can assign inventory viewing and modification roles.",
        observer_role_name: "For a given location, can observe inventory.",
        inbound_role_name: "For a given location, can add inbound items to inventory.",
        outbound_role_name: "For a given location, can remove outbound items from inventory.",
        transfer_role_name: "For a given location, can transfer items out of inventory to another location.",
        adjust_role_name: "For a given location, can adjust inventory amounts to match hand counts.",
        super_role_name: "Has top level authority to make changes.",
        people_viewer_name: "Can view some user accounts.",
        roots_observer_role_name: "Can view organizations.",
        self_role_name: "Can look at own user account.",
        anybody_role_name: "Things anybody is allowed to do.",
    }

    universal_role_name_set = {user_admin_role_name}
    root_role_name_set = {admin_role_name, linkage_role_name, structuring_role_name, structure_viewer_role_name}
    place_role_name_set = {location_manager_name, inventory_manager_name, observer_role_name, inbound_role_name,
                           outbound_role_name, transfer_role_name, adjust_role_name}
    pseudo_role_name_set = {anybody_role_name, super_role_name, self_role_name, people_viewer_name,
                            roots_observer_role_name}

    universal_role_name_list = sorted(universal_role_name_set)
    root_role_name_list = sorted(root_role_name_set)
    place_role_name_list = sorted(place_role_name_set)
    pseudo_role_name_list = sorted(pseudo_role_name_set)

    role_name_list = universal_role_name_list + root_role_name_list + place_role_name_list

    @property
    def parent_object(self):
        return AllRoles()

    @property
    def identities(self):
        return {'role_id': self.id}

    @property
    def is_observer_role(self):
        return self.is_named(self.observer_role_name)

    def is_named(self, name_of_role):
        return self.name == name_of_role


def all_roles():
    # Todo use all type query, then sort by name
    return [find_role(name) for name in Role.role_name_list]


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
        find_or_create_role(name=name, description=Role.role_descriptions[name])
        for name in Role.role_name_list
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
