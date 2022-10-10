from werkzeug.security import check_password_hash

from tracking import database
from tracking.people.people_models import find_or_create_user
from old_testing.fixtures_for_testing import app, curly_stooge_user, generate_curly, CURLY_STOOGE_USER_NAME


def _pycharm_please_keep_these_imports():
    return app, curly_stooge_user




def test_user_generation(app):
    user = generate_curly()
    assert user is not None
    assert user.first_name == u'Curly'
    assert user.last_name == u'Stooge'
    assert user.username == CURLY_STOOGE_USER_NAME
    assert check_password_hash(user.password, 'YukYuk12345')
    assert not user.is_admin
    assert user.date_joined.year == 1941
    assert user.id is None


def test_stooge_user(curly_stooge_user):
    assert curly_stooge_user.first_name == u'Curly'
    assert curly_stooge_user.last_name == u'Stooge'
    assert curly_stooge_user.username == CURLY_STOOGE_USER_NAME
    assert check_password_hash(curly_stooge_user.password, 'YukYuk12345')
    assert not curly_stooge_user.is_admin
    assert curly_stooge_user.date_joined.year == 1941
    assert curly_stooge_user.id is not None


def test_stooge_user_again(curly_stooge_user):
    assert curly_stooge_user.id is not None


def test_find_or_create_user_no_user(app):
    new_user = find_or_create_user(u'Larry', u'Stooge', u'larry', 'YukYuk12345')
    assert new_user.username == u'larry'
    assert new_user.id is None
    database.session.commit()
    old_user = find_or_create_user(u'Larry', u'Stooge', u'larry', 'YukYuk12345')
    assert old_user.username == u'larry'
    assert old_user.id is not None
