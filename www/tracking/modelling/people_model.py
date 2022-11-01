#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ

from flask import url_for
from flask_login import UserMixin
from sqlalchemy import event
from werkzeug.security import generate_password_hash

from tracking import database
from tracking.contexts.cupboard_display_context import CupboardDisplayContext, CupboardDisplayContextMixin
from tracking.modelling.base_models import IdModelMixin
from tracking.modelling.cardistry_models import name_is_key, bread_crumbs


class AllPeople:
    label = 'People'


class User(CupboardDisplayContextMixin, IdModelMixin, database.Model, UserMixin):
    """ User acts on behalf of various groups """

    singular_label = "Person"
    plural_label = "People"
    possible_tasks = ['update', 'delete']
    label_prefixes = {}
    flavor = "people"

    # User authentication fields
    username = database.Column(database.String(255), nullable=False, unique=True)
    password = database.Column(database.String(255), nullable=False)

    # User fields
    is_admin = database.Column(database.Boolean(), nullable=False, default=False)
    first_name = database.Column(database.Unicode(50), nullable=False, server_default=u'')
    last_name = database.Column(database.Unicode(50), nullable=False, server_default=u'')
    date_joined = database.Column(database.DateTime(), default=datetime.now())
    about_me = database.Column(database.Text(), nullable=False, server_default=u'')

    root_assignments = database.relationship('RootAssignment', backref='person', lazy=True, cascade='all, delete')
    place_assignments = database.relationship('PlaceAssignment', backref='person', lazy=True, cascade='all, delete')
    universal_assignments = database.relationship('UniversalAssignment', backref='person', lazy=True,
                                                  cascade='all, delete')

    @property
    def identities(self):
        return {'user_id': self.id}

    def viewable_children(self, viewer):
        return []

    def add_description(self, display_context):
        display_context.add_multiline_notation(label="About me", multiline=self.about_me)

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [AllPeople, self], target=self)

    def may_perform_task(self, viewer, task):
        if task == 'view':
            return viewer.may_observe_people
        elif task == 'delete':
            return viewer.may_delete_person(self)
        elif task == 'update':
            return viewer.may_update_person(self)
        elif task == 'create':
            return viewer.may_create_person
        else:
            return False

    @property
    def may_create_root(self):
        return self.is_the_super_admin

    @property
    def may_delete_root(self):
        return self.is_the_super_admin

    @property
    def may_update_root(self):
        return self.is_the_super_admin

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
        return f'{self.first_name} {self.last_name}'

    @property
    def may_edit_database(self):
        return self.is_the_super_admin

    @property
    def may_assign_universal_roles(self):
        return self.is_an_admin

    @property
    def may_create_place(self):
        return self.is_an_admin

    @property
    def may_delete_place(self):
        return self.is_an_admin

    @property
    def may_update_place(self):
        return self.is_an_admin

    @property
    def may_create_person(self):
        return self.is_an_admin

    def may_update(self, viewer):
        return viewer.may_update_person(self)

    def may_update_person(self, person):
        return self.is_an_admin or self == person

    @property
    def may_create_thing(self):
        return self.is_an_admin

    @property
    def may_delete_thing(self):
        return self.is_an_admin

    @property
    def may_update_thing(self):
        return self.is_an_admin

    @property
    def may_create_category(self):
        return self.is_an_admin

    @property
    def may_delete_category(self):
        return self.is_an_admin

    @property
    def may_delete_choice(self):
        return self.is_an_admin

    @property
    def may_update_category(self):
        return self.is_an_admin

    @property
    def may_update_choice(self):
        return self.is_an_admin

    @property
    def may_create_role(self):
        return self.is_the_super_admin

    def may_delete_person(self, person):
        # Super admin cannot be deleted.
        return self.is_an_admin and not person.is_the_super_admin

    @property
    def may_observe_people(self):
        # TODO: refine this
        return self.may_observe

    @property
    def may_observe_categories(self):
        # TODO: refine this
        return self.may_observe

    @property
    def may_observe_groups(self):
        # TODO: refine this
        return self.may_observe

    @property
    def may_observe_places(self):
        # TODO: refine this
        return self.may_observe

    @property
    def may_observe_things(self):
        # TODO: refine this
        return self.may_observe

    @property
    def may_observe(self):
        def yes(assignment):
            return assignment.is_observer

        return self.is_an_admin or any(map(yes, self.assignments))

    def has_role(self, root_or_place, name_of_role):
        return self.has_universal_role(name_of_role) or root_or_place.has_role(self, name_of_role)

    def has_universal_role(self, name_of_role):
        def yes(assignment):
            return assignment.is_named(name_of_role)

        return any(map(yes, self.universal_assignments))

    def may_view_person(self, user):
        return self.is_the_super_admin or not user.is_the_super_admin

    def may_be_observed(self, viewer):
        return viewer.is_the_super_admin or not self.is_the_super_admin

    @property
    def label(self):
        return self.name

    @property
    def url(self):
        return url_for('people_bp.people_view', user_id=self.id)

    @property
    def deletion_url(self):
        return url_for('people_bp.people_delete', user_id=self.id)

    @property
    def viewable_categories(self):
        from tracking.modelling.category_model import all_categories
        return [category.viewable_attributes(self) for category in all_categories() if category.user_may_view(self)]


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


def find_user_by_username(username):
    return User.query.filter(User.username == username).first()


def find_user_by_id(user_id):
    return User.query.filter(User.id == user_id).first()


def create_test_users():
    find_or_create_user('Curly', 'Stooge', 'curly', 'aaaaaa', is_admin=False, about_me='Bald headed stooge')
    find_or_create_user('Moe', 'Stooge', 'moe', 'aaaaaa', is_admin=True, about_me="top stooge")
    find_or_create_user('Larry', 'Stooge', 'larry', 'aaaaaa', is_admin=False, about_me="One\nOf\nThe\nThree Stooges")


def create_initial_users():
    """ Create users """
    create_initial_admin()

    if environ.get('TEST_USERS') or environ.get('ADD_TEST_DATA'):
        create_test_users()


def create_initial_admin():
    find_or_create_user(u'Website', u'Admin', u'admin', '23Skid00', is_admin=True)


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
    context = CupboardDisplayContext()
    context['flavor'] = User.flavor
    context['label'] = User.plural_label
    if viewer.may_observe_people:
        for person in all_people():
            context.add_notation(label=person.singular_label, url=navigator.url(person, 'view'), value=person.name)
    if viewer.may_create_person:
        context.add_task(url=navigator.url(User, 'create'), label="User Account", task='create')
    return context
