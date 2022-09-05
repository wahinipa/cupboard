#  Copyright (c) 2022. Wahinipa LLC
from testing.fixtures_for_testing import app, curly_stooge_user, CURLY_STOOGE_USER_NAME


def _pycharm_please_keep_these_imports():
    return app, curly_stooge_user


def test_user_creation(curly_stooge_user):
    assert curly_stooge_user.username == CURLY_STOOGE_USER_NAME
