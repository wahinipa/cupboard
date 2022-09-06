#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ, path, remove

import pytest

from tracking import create_app, database
#############################
# Application Test Fixtures #
#############################
from tracking.groups.group_models import create_group
from tracking.people.people_models import find_or_create_user
from tracking.places.place_models import create_place
from tracking.things.thing_models import create_thing


@pytest.fixture
def app():
    app = create_app()
    if environ.get('TEST_SQL_IN_MEMORY') != 'True':
        basedir = path.abspath(path.dirname(__file__))
        test_data_base = path.join(basedir, 'cupboard_test.db')
        remove(test_data_base)
    yield app


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


class PretendApplication:
    def __init__(self):
        self.blueprints = {}

    def register_blueprint(self, blueprint, url_prefix=None):
        blueprint_name = blueprint.name
        self.blueprints[blueprint_name] = {
            "blueprint": blueprint,
            "url_prefix": url_prefix
        }


@pytest.fixture
def pretend_application():
    return PretendApplication()


######################
# User Test Fixtures #
######################

CURLY_STOOGE_USER_NAME = u'user_is_curly'
CURLY_STOOGE_FULL_NAME = u'Curly Stooge'

LARRY_STOOGE_USER_NAME = u'user_is_larry'
LARRY_STOOGE_FULL_NAME = u'Curly Stooge'

MOE_STOOGE_USER_NAME = u'user_is_moe'
MOE_STOOGE_FULL_NAME = u'Moe Stooge'


def generate_curly():
    date_joined = datetime(1941, 12, 7)
    return find_or_create_user(u'Curly', u'Stooge', CURLY_STOOGE_USER_NAME, 'YukYuk12345', False, date_joined)


def generate_larry():
    date_joined = datetime(1951, 12, 7)
    return find_or_create_user(u'Larry', u'Stooge', LARRY_STOOGE_USER_NAME, 'YakYak12345', False, date_joined)


def generate_moe():
    date_joined = datetime(1961, 12, 7)
    return find_or_create_user(u'Moe', u'Stooge', MOE_STOOGE_USER_NAME, 'YekYek12345', False, date_joined)


@pytest.fixture()
def curly_stooge_user(app):
    curly = generate_curly()
    database.session.add(curly)
    database.session.commit()
    return curly


@pytest.fixture()
def larry_stooge_user(app):
    larry = generate_larry()
    database.session.add(larry)
    database.session.commit()
    return larry


@pytest.fixture()
def moe_stooge_user(app):
    moe = generate_moe()
    database.session.commit()
    return moe


#######################
# Group Test Fixtures #
#######################

GROUP_NAME = "Knights of the Round Table"
GROUP_DESCRIPTION = "Always rescuing thine maidens, fair or not"
GROUP_DATE = datetime(1994, 6, 12)


@pytest.fixture()
def knights_of_the_round_table(app):
    return create_group(GROUP_NAME, GROUP_DESCRIPTION, date_created=GROUP_DATE)


#######################
# Place Test Fixtures #
#######################

PLACE_NAME = "Over the Rainbow"
PLACE_DESCRIPTION = "Follow the yellow brick road."
PLACE_DATE = datetime(2022, 6, 18)


@pytest.fixture()
def rainbow_place(app, knights_of_the_round_table):
    return create_place(knights_of_the_round_table, PLACE_NAME, PLACE_DESCRIPTION, date_created=PLACE_DATE)


#######################
# Thing Test Fixtures #
#######################

THING_NAME = "Light Saber"
THING_DESCRIPTION = "Useful for defeating galactic tyranny."
THING_DATE = datetime(1984, 1, 1)


@pytest.fixture()
def light_saber(app):
    return create_thing(THING_NAME, THING_DESCRIPTION, date_created=THING_DATE)
