#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from tracking import database
from tracking.commons.base_models import IdModelMixin


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
    def is_the_admin(self):
        return self.username == 'admin'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def has_role(self, group_or_place, name_of_role):
        return self.has_universal_role(name_of_role) or group_or_place.has_role(self, name_of_role)

    def has_universal_role(self, name_of_role):
        for assignment in self.universal_assignments:
            if assignment.role.name == name_of_role:
                return True
        return False


def load_user(unicode_user_id):
    try:
        integer_id = int(unicode_user_id)
        return User.query.filter(User.id == integer_id).first()
    except:
        return None


def find_user_by_username(username):
    return User.query.filter(User.username == username).first()


def create_initial_users():
    """ Create users """
    create_initial_admin()


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
                password=generate_password_hash(password),
                is_admin=is_admin,
                date_joined=date_joined)
    return user
