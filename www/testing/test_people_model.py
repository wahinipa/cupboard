#  Copyright (c) 2022, Wahinipa LLC
from werkzeug.security import check_password_hash

from testing.fixtures import app, curly_stooge_user, CURLY_STOOGE_USER_NAME
from tracking import database
from tracking.modelling.people_model import find_or_create_user


def _pycharm_please_keep_these_imports():
    return app, curly_stooge_user


def test_user_creation(curly_stooge_user):
    assert curly_stooge_user.username == CURLY_STOOGE_USER_NAME
    assert curly_stooge_user is not None
    assert curly_stooge_user.first_name == u'Curly'
    assert curly_stooge_user.last_name == u'Stooge'
    assert curly_stooge_user.username == CURLY_STOOGE_USER_NAME
    assert check_password_hash(curly_stooge_user.password, 'YukYuk12345')
    assert not curly_stooge_user.is_admin
    assert curly_stooge_user.date_joined.year == 1941

def test_stooge_user_again(curly_stooge_user):
    assert curly_stooge_user.id is not None

def test_disable_user(curly_stooge_user):
    assert curly_stooge_user.is_active
    curly_stooge_user.disable()
    assert not curly_stooge_user.is_active
    curly_stooge_user.enable()
    assert curly_stooge_user.is_active


def test_find_or_create_user_no_user(app):
    new_user = find_or_create_user(u'Larry', u'Stooge', u'larry', 'YukYuk12345')
    assert new_user.username == u'larry'
    assert new_user.id is None
    database.session.commit()
    old_user = find_or_create_user(u'Larry', u'Stooge', u'larry', 'YukYuk12345')
    assert old_user.username == u'larry'
    assert old_user.id is not None
