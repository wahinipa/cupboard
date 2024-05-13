#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from sqlalchemy.orm import declared_attr

from tracking import database
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.base_models import DatedModelMixin, IdModelMixin, UniqueNamedBaseModel


class Role(CupboardDisplayContextMixin, UniqueNamedBaseModel):
    """
    A Role is a simple named and described object that is used to determine what a signed-in user may or may not do.
    The critical part of a Role is its name.
    The unique name is used in the logic that makes decisions about permissions.
    A Role is assigned to a User in three different ways:
        RootAssignment gives the user that Role for a particular Root and all of its Places.
        PlaceAssignment gives the user that Role for a particular Place and all of its contained (child) Places.
        UniversalAssignment gives the user that Role without regard to Root or Place.
    """
    plural_label = "Roles"
    possible_tasks = []
    label_prefixes = {}
    flavor = 'role'
    root_assignments = database.relationship('RootAssignment', backref='role', lazy=True, cascade='all, delete')
    place_assignments = database.relationship('PlaceAssignment', backref='role', lazy=True, cascade='all, delete')
    universal_assignments = database.relationship('UniversalAssignment', backref='role', lazy=True,
                                                  cascade='all, delete')

    # The following names are used to define roles in the actual application.
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

    # These pseudo-role names do not refer to Role objects so do not appear in Assignments.
    # They are convenient in the constuction of the user interface.
    # For example self_role_name is used to allow a User to modify their own "About Me".
    super_role_name = "Super Admin"  # No actual Role created for this
    self_role_name = "Viewer is Self"  # No actual Role created for this
    people_viewer_name = "Viewer of People"  # No actual Role created for this
    roots_observer_role_name = "Viewer of Roots"  # No actual Role created for this
    anybody_role_name = "Anybody"  # No actual Role created for this
    control_role_name = "Control"  # No actual Role created for this

    # This dictionary provides useful Role descriptions from the Role (or pseudo-role) names.
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
        control_role_name: "Control Pseudo Role.",
    }

    # Names of Roles that can be Universal
    universal_role_name_set = {user_admin_role_name}

    # Names of Roles that can be attached to a Root.
    root_role_name_set = {admin_role_name, linkage_role_name, structuring_role_name, structure_viewer_role_name}

    # Names of Roles that can be attached to a Place.
    place_role_name_set = {location_manager_name, inventory_manager_name, observer_role_name, inbound_role_name,
                           outbound_role_name, transfer_role_name, adjust_role_name}

    # Names of Pseudo-roles that do not create Role objects.
    pseudo_role_name_set = {anybody_role_name, super_role_name, self_role_name, people_viewer_name,
                            roots_observer_role_name, control_role_name}

    # The above sets of role names listed in alphabetical order.
    universal_role_name_list = sorted(universal_role_name_set)
    root_role_name_list = sorted(root_role_name_set)
    place_role_name_list = sorted(place_role_name_set)
    pseudo_role_name_list = sorted(pseudo_role_name_set)

    # A list of all the role names for actual Roles (excludes pseudo-roles).
    role_name_list = universal_role_name_list + root_role_name_list + place_role_name_list

    # For a given Role, which Roles allow a User to grant that power to another User?
    granting_powers = {
        user_admin_role_name: [super_role_name],
        admin_role_name: [super_role_name],
        linkage_role_name: [admin_role_name, super_role_name],
        structuring_role_name: [admin_role_name, super_role_name],
        structure_viewer_role_name: [admin_role_name, super_role_name],
        location_manager_name: [admin_role_name, super_role_name],
        inventory_manager_name: [location_manager_name, admin_role_name, super_role_name],
        observer_role_name: [inventory_manager_name],
        inbound_role_name: [inventory_manager_name],
        outbound_role_name: [inventory_manager_name],
        transfer_role_name: [inventory_manager_name],
        adjust_role_name: [inventory_manager_name],
    }

    @property
    def singular_label(self):
        role_name = self.name
        if role_name in self.universal_role_name_set:
            return 'Universal Role'
        elif role_name in self.root_role_name_set:
            return 'Organization Role'
        elif role_name in self.place_role_name_set:
            return 'Place Role'
        else:
            return 'Role'

    @property
    def parent_object(self):
        from tracking.viewers.all_roles import AllRoles
        return AllRoles()  # Pseudo object that acts the parent to all the roles.

    @property
    def identities(self):
        """ returns dictionary needed when constructing urls for role tasks """
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
    __abstract__ = True  # Used as base class, not an actual database table.

    @declared_attr
    def role_id(cls):
        return database.Column(database.Integer, database.ForeignKey('role.id'))

    @declared_attr
    def person_id(cls):
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


def remove_role(role, user, place=None, root=None):
    root = root or (place and place.root)
    place = place or (root and root.place)
    for assignment in user.universal_assignments:
        if assignment.role == role:
            database.session.delete(assignment)
            database.session.commit()
            return
    if root:
        for assignment in user.root_assignments:
            if assignment.role == role and assignment.root == root:
                database.session.delete(assignment)
                database.session.commit()
                return
    if place:
        for assignment in user.place_assignments:
            if assignment.role == role and assignment.place == place:
                database.session.delete(assignment)
                database.session.commit()
                return
