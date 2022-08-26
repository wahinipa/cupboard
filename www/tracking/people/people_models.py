# Copyright 2022 Wahinipa LLC
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from www.tracking import database


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)

    # User authentication fields
    username = database.Column(database.String(255), nullable=False, unique=True)
    password = database.Column(database.String(255), nullable=False)

    # User fields
    is_admin = database.Column(database.Boolean(), nullable=False, default=False)
    first_name = database.Column(database.Unicode(50), nullable=False, server_default=u'')
    last_name = database.Column(database.Unicode(50), nullable=False, server_default=u'')
    date_joined = database.Column(database.DateTime(), default=datetime.now())
    about_me = database.Column(database.String(255), nullable=False, server_default=u'')



def load_user(unicode_user_id):
    try:
        integer_id = int(unicode_user_id)
        return User.query.filter(User.id == integer_id).first()
    except:
        return None

