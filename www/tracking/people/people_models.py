#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ

from flask import url_for
from flask_login import UserMixin
from sqlalchemy import event
from werkzeug.security import generate_password_hash

from tracking import database
from tracking.commons.base_models import IdModelMixin, name_is_key
from tracking.commons.display_context import DisplayContext


class AllPeople:
    def __init__(self):
        self.label = "People"

    @property
    def url(self):
        return url_for('people_bp.people_list')


class User(IdModelMixin, database.Model, UserMixin):
    """ User acts on behalf of various groups """

    # User authentication fields
    username = database.Column(database.String(255), nullable=False, unique=True)
    password = database.Column(database.String(255), nullable=False)

    # User fields
    is_admin = database.Column(database.Boolean(), nullable=False, default=False)
    first_name = database.Column(database.Unicode(50), nullable=False, server_default=u'')
    last_name = database.Column(database.Unicode(50), nullable=False, server_default=u'')
    date_joined = database.Column(database.DateTime(), default=datetime.now())
    about_me = database.Column(database.String(255), nullable=False, server_default=u'')

    group_assignments = database.relationship('GroupAssignment', backref='person', lazy=True, cascade='all, delete')
    place_assignments = database.relationship('PlaceAssignment', backref='person', lazy=True, cascade='all, delete')
    universal_assignments = database.relationship('UniversalAssignment', backref='person', lazy=True,
                                                  cascade='all, delete')

    @property
    def assignments(self):
        return self.universal_assignments + self.group_assignments + self.place_assignments

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
    def may_create_group(self):
        return self.is_an_admin

    @property
    def may_delete_group(self):
        return self.is_an_admin

    @property
    def may_update_group(self):
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

    def has_role(self, group_or_place, name_of_role):
        return self.has_universal_role(name_of_role) or group_or_place.has_role(self, name_of_role)

    def has_universal_role(self, name_of_role):
        def yes(assignment):
            return assignment.is_named(name_of_role)

        return any(map(yes, self.universal_assignments))

    def may_view_person(self, user):
        return self.is_the_super_admin or not user.is_the_super_admin

    @property
    def parent_list(self):
        return [AllPeople()]

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
        from tracking.categories.category_models import all_categories
        return [category.viewable_attributes(self) for category in all_categories() if category.user_may_view(self)]

    @property
    def viewable_groups(self):
        from tracking.groups.group_models import all_groups
        return [group.viewable_attributes(self) for group in all_groups() if group.user_may_view(self)]

    @property
    def viewable_places(self):
        from tracking.groups.group_models import all_groups
        result = []
        for group in all_groups():
            if group.user_may_view(self):
                for place in group.sorted_places:
                    result.append(place.viewable_attributes(self, include_group_url=True))
        return result

    @property
    def viewable_people(self):
        return [person.viewable_attributes(self) for person in all_people() if self.may_view_person(person)]

    def viewable_attributes(self, viewer):
        attributes = {
            'name': self.name,
            'url': self.url,
            'about_me': self.about_me,
        }
        return attributes

    def display_context(self, viewer):
        person_context = DisplayContext({
            'person': self.viewable_attributes(viewer),
            'name': self.name,
            'label': self.label,
            'parent_list': self.parent_list,
        })
        if viewer.may_delete_person(self):
            person_context.add_action(self.deletion_url, self.name, 'delete')
        return person_context.display_context


def people_list_display_context(viewer):
    category_context = DisplayContext({
        'tab': 'people',
        'label': 'People',
        'name': 'People',
        'people': viewer.viewable_people,
    })
    if viewer.may_create_person:
        category_context.add_action(url_for('people_bp.create'), 'User Account', 'create')
    return category_context.display_context


def all_people():
    return sorted(User.query.all(), key=name_is_key)


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
    find_or_create_user('Curly', 'Stooge', 'curly', 'aaaaaa', is_admin=False)
    find_or_create_user('Moe', 'Stooge', 'moe', 'aaaaaa', is_admin=True)
    find_or_create_user('Larry', 'Stooge', 'larry', 'aaaaaa', is_admin=False)


def create_initial_users():
    """ Create users """
    create_initial_admin()

    if environ.get('TEST_USERS') or environ.get('ADD_TEST_DATA'):
        create_test_users()


def create_initial_admin():
    find_or_create_user(u'Website', u'Admin', u'admin', '23Skid00', is_admin=True)


def find_or_create_user(first_name, last_name, username, password, is_admin=False, date_joined=None):
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
                                         date_joined=date_joined
                                         )
        database.session.add(user)
    return user


def generate_uncommitted_user(first_name, last_name, username, password, is_admin, date_joined):
    user = User(username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_admin=is_admin,
                date_joined=date_joined)
    return user
