# Copyright 2022 Wahinipa LLC
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from www.tracking.commons.builder import database


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)

    # User authentication fields
    username = database.Column(database.String(255), nullable=False, unique=True)
    password = database.Column(database.String(255), nullable=False)

    # User fields
    is_admin = database.Column(database.Boolean(), nullable=False, default=False)
    first_name = database.Column(database.Unicode(50), nullable=False, server_default='')
    last_name = database.Column(database.Unicode(50), nullable=False, server_default='')
    date_joined = database.Column(database.DateTime(), default=datetime.now())
    about_me = database.Column(database.String(255), nullable=False, server_default='')


def load_user(unicode_user_id):
    try:
        integer_id = int(unicode_user_id)
        return User.query.filter(User.id == integer_id).first()
    except:
        return None


def find_user_by_username(username):
    return User.query.filter(User.username == username).first()

def find_or_create_user(first_name, last_name, username, password, is_admin=False, date_joined=None):
    pass
    """ Find existing user or create new user """
    user = User.query.filter(User.username == username).first()
    if not user:
        if date_joined is None:
            date_joined = datetime.now()
        user = User(username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=generate_password_hash(password),
                    is_admin=is_admin,
                    date_joined=date_joined)
        database.session.add(user)
    return user


