#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ

from flask_login import UserMixin
from sqlalchemy import event
from werkzeug.security import generate_password_hash

from tracking import database
from tracking.contexts.cupboard_display_context import CupboardDisplayContext, CupboardDisplayContextMixin
from tracking.modelling.base_models import IdModelMixin
from tracking.modelling.cardistry_models import bread_crumbs, name_is_key
from tracking.modelling.linkage_model import Linkage
from tracking.modelling.role_models import Role, assign_universal_role, find_or_create_role


class AllPeople:
    label = 'People'
    id = 0


class User(CupboardDisplayContextMixin, IdModelMixin, database.Model, UserMixin):
    """ User acts on behalf of various groups """

    @property
    def is_active(self):
        return self.is_enabled

    singular_label = "Person"
    plural_label = "People"
    possible_tasks = ['update', 'delete', 'enable', 'disable']
    label_prefixes = {}
    flavor = "people"

    # User authentication fields
    username = database.Column(database.String(255), nullable=False, unique=True)
    password = database.Column(database.String(255), nullable=False)

    # User fields
    is_enabled = database.Column(database.Boolean(), nullable=False, default=True)
    is_admin = database.Column(database.Boolean(), nullable=False, default=False)
    first_name = database.Column(database.Unicode(50), nullable=False, server_default=u'')
    last_name = database.Column(database.Unicode(50), nullable=False, server_default=u'')
    date_joined = database.Column(database.DateTime(), default=datetime.now())
    about_me = database.Column(database.Text(), nullable=False, server_default=u'')

    linkages = database.relationship('Linkage', backref='person', lazy=True, cascade='all, delete')
    root_assignments = database.relationship('RootAssignment', backref='person', lazy=True, cascade='all, delete')
    place_assignments = database.relationship('PlaceAssignment', backref='person', lazy=True, cascade='all, delete')
    universal_assignments = database.relationship('UniversalAssignment', backref='person', lazy=True,
                                                  cascade='all, delete')

    @property
    def identities(self):
        return {'person_id': self.id}

    def viewable_children(self, viewer):
        return []

    @property
    def sorted_roles_per_place(self):
        roles_per_place = {}
        for assignment in self.place_assignments:
            roles_per_place.setdefault(assignment.place.name, []).append(assignment.role.name)
        sorted_place_names = sorted(roles_per_place.keys())
        return [(place_name, sorted(roles_per_place[place_name])) for place_name in sorted_place_names]

    @property
    def sorted_roles_per_root(self):
        roles_per_root = {}
        for assignment in self.root_assignments:
            roles_per_root.setdefault(assignment.root.name, []).append(assignment.role.name)
        sorted_root_names = sorted(roles_per_root.keys())
        return [(root_name, sorted(roles_per_root[root_name])) for root_name in sorted_root_names]

    def add_description(self, display_context):
        display_context.add_notation(label="Username", value=self.username)
        for linkage in self.linkages:
            display_context.add_notation(label="Association", value=linkage.root.name)
        display_context.add_multiline_notation(label="About me", multiline=self.about_me)
        if self.is_the_super_admin:
            display_context.add_role_description(Role.super_role_name)
        for role_name in Role.universal_role_name_list:
            if self.has_universal_role(role_name):
                display_context.add_role_description(role_name)
        for root_name, role_name_list in self.sorted_roles_per_root:
            for role_name in role_name_list:
                suffix = f' for {root_name}'
                display_context.add_role_description(role_name, suffix=suffix)
        for place_name, role_name_list in self.sorted_roles_per_place:
            for role_name in role_name_list:
                suffix = f' at {place_name}'
                display_context.add_role_description(role_name, suffix=suffix)


    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [AllPeople, self], target=self)

    def link_to_root(self, root):
        if not self.is_linked(root):
            link = Linkage(person=self, root=root)
            database.session.add(link)
            database.session.commit()

    def unlink_from_root(self, root):
        commit = False
        for link in self.linkages:
            if link.root == root:
                database.session.delete(link)
                commit = True
        if commit:
            database.session.commit()

    def is_linked(self, root):
        for link in self.linkages:
            if link.root == root:
                return True
        return False

    #### ????? ####

    @property
    def assignments(self):
        return self.universal_assignments + self.root_assignments + self.place_assignments

    @property
    def is_the_super_admin(self):
        return self.username == 'admin'

    @property
    def is_an_admin(self):
        return self.is_the_super_admin or self.is_admin

    @property
    def name(self):
        name = f'{self.first_name} {self.last_name}'
        if not self.is_active:
            name += ' (inactive)'
        return name

    @property
    def may_edit_database(self):
        return self.is_the_super_admin

    def has_role(self, root_or_place, name_of_role):
        return self.has_universal_role(name_of_role) or root_or_place.has_role(self, name_of_role)

    def has_universal_role(self, name_of_role):
        def yes(assignment):
            return assignment.is_named(name_of_role)

        return any(map(yes, self.universal_assignments))

    def has_exact_role(self, name_of_role, root=None, place=None):
        for assignment in self.universal_assignments:
            if assignment.role.name == name_of_role:
                return True
        root = root or (place and place.root)
        if root:
            for assignment in self.root_assignments:
                if assignment.role.name == name_of_role and assignment.root == root:
                    return True
        place = place or (root and root.place)
        if place:
            for assignment in self.place_assignments:
                if assignment.role.name == name_of_role and assignment.place == place:
                    return True
        return False

    @property
    def label(self):
        return self.name

    @property
    def roots(self):
        if self.is_the_super_admin:
            from tracking.modelling.root_model import all_roots
            return all_roots()
        else:
            return [link.root for link in self.linkages]

    @property
    def only_root(self):
        if not self.is_the_super_admin:
            roots = self.roots
            if len(roots) == 1:
                return roots[0]
        return None

    @property
    def is_rootless(self):
        return self.roots is None or 0 == len(self.roots)

    def disable(self):
        self.is_enabled = False

    def enable(self):
        self.is_enabled = True


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


def load_user(unicode_user_id):
    try:
        integer_id = int(unicode_user_id)
        return User.query.filter(User.id == integer_id).first()
    except:
        return None


def find_person_by_username(username):
    return User.query.filter(User.username == username).first()


def find_person_by_id(person_id):
    return User.query.filter(User.id == person_id).first()


def create_test_users():
    return [
        find_or_create_user('Curly', 'Stooge', 'curly', 'aaaaaa', is_admin=False, about_me='Bald headed stooge'),
        find_or_create_user('Moe', 'Stooge', 'moe', 'aaaaaa', is_admin=True, about_me="top stooge"),
        find_or_create_user('Larry', 'Stooge', 'larry', 'aaaaaa', is_admin=False,
                            about_me="One\nOf\nThe\nThree Stooges"),
    ]


def create_initial_users():
    """ Create users """
    created_users = [create_initial_admin()]

    if environ.get('TEST_USERS') or environ.get('ADD_TEST_DATA'):
        created_users += create_test_users()

    return created_users


def create_initial_admin():
    super_admin = find_or_create_user(u'Website', u'Admin', u'admin', '23Skid00', is_admin=True)
    user_admin_role = find_or_create_role(Role.user_admin_role_name)
    assign_universal_role(user_admin_role, super_admin)
    return super_admin


def find_or_create_user(first_name, last_name, username, password, is_admin=False, date_joined=None, about_me=''):
    """ Find existing user or create new user """
    user = User.query.filter(User.username == username).first()
    if not user:
        if date_joined is None:
            date_joined = datetime.now()
        user = generate_uncommitted_user(username=username,
                                         first_name=first_name,
                                         last_name=last_name,
                                         password=password,
                                         is_admin=is_admin,
                                         about_me=about_me,
                                         date_joined=date_joined
                                         )
        database.session.add(user)
    return user

def reset_pw(username, new_pw):
    user = User.query.filter(User.username == username).first()
    if user:
        user.password = new_pw
        database.session.commit()


def generate_uncommitted_user(first_name, last_name, username, password, is_admin, about_me, date_joined):
    user = User(username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_admin=is_admin,
                about_me=about_me,
                date_joined=date_joined)
    return user


def all_people():
    return sorted(User.query.all(), key=name_is_key)


def all_people_display_context(navigator, viewer):
    context = CupboardDisplayContext(viewer)
    context['flavor'] = User.flavor
    context['label'] = User.plural_label
    if viewer.may_observe_people:
        for person in all_people():
            context.add_notation(label=person.singular_label, url=navigator.target_url(person, 'view'),
                                 value=person.name)
    if viewer.may_create_person:
        context.add_task(url=navigator.target_url(User, 'create'), label="User Account", task='create')
    return context
