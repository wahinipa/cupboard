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
from tracking.roles.role_models import create_role
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

ROUND_TABLE_GROUP_NAME = "Knights of the Round Table"
ROUND_TABLE_DESCRIPTION = "Always rescuing thine maidens, fair or not"
ROUND_TABLE_DATE = datetime(1994, 6, 12)

QUEENS_TABLE_GROUP_NAME = "Queens of the Square Table"
QUEENS_TABLE_DESCRIPTION = "Bunch of Snoots"
QUEENS_TABLE_DATE = datetime(1993, 5, 10)


@pytest.fixture()
def knights_of_the_round_table(app):
    return create_group(ROUND_TABLE_GROUP_NAME, ROUND_TABLE_DESCRIPTION, date_created=ROUND_TABLE_DATE)

@pytest.fixture()
def queens_of_the_round_table(app):
    return create_group(QUEENS_TABLE_GROUP_NAME, QUEENS_TABLE_DESCRIPTION, date_created=QUEENS_TABLE_DATE)


#######################
# Role Test Fixtures #
#######################

DUNCE_ROLE_NAME = "Dunce"
DUNCE_DESCRIPTION = "Does really stupid things."
DUNCE_DATE = datetime(1925, 2, 5)

BUFFOON_ROLE_NAME = "Buffoon"
BUFFOON_DESCRIPTION = "Does really silly things."
BUFFOON_DATE = datetime(1926, 3, 6)

BOSSY_ROLE_NAME = "Bossy"
BOSSY_DESCRIPTION = "Does really bossy things."
BOSSY_DATE = datetime(1927, 7, 17)

@pytest.fixture()
def dunce(app):
    return create_role(DUNCE_ROLE_NAME, DUNCE_DESCRIPTION, DUNCE_DATE)

@pytest.fixture()
def buffoon(app):
    return create_role(BUFFOON_ROLE_NAME, BUFFOON_DESCRIPTION, BUFFOON_DATE)

@pytest.fixture()
def bossy(app):
    return create_role(BOSSY_ROLE_NAME, BOSSY_DESCRIPTION, BOSSY_DATE)

@pytest.fixture()
def light_saber(app):
    return create_thing(THING_NAME, THING_DESCRIPTION, date_created=THING_DATE)

#######################
# Place Test Fixtures #
#######################

RAINBOW_PLACE_NAME = "Over the Rainbow"
RAINBOW_PLACE_DESCRIPTION = "Follow the yellow brick road."
RAINBOW_PLACE_DATE = datetime(2022, 6, 18)

WILD_PLACE_NAME = "Over on the Wild Side"
WILD_PLACE_DESCRIPTION = "Listen to your Mama."
WILD_PLACE_DATE = datetime(2020, 5, 18)


@pytest.fixture()
def rainbow_place(app, knights_of_the_round_table):
    return create_place(knights_of_the_round_table, RAINBOW_PLACE_NAME, RAINBOW_PLACE_DESCRIPTION, date_created=RAINBOW_PLACE_DATE)

@pytest.fixture()
def wild_place(app, knights_of_the_round_table):
    return create_place(knights_of_the_round_table, RAINBOW_PLACE_NAME, RAINBOW_PLACE_DESCRIPTION, date_created=RAINBOW_PLACE_DATE)


#######################
# Thing Test Fixtures #
#######################

THING_NAME = "Light Saber"
THING_DESCRIPTION = "Useful for defeating galactic tyranny."
THING_DATE = datetime(1984, 1, 1)


@pytest.fixture()
def light_saber(app):
    return create_thing(THING_NAME, THING_DESCRIPTION, date_created=THING_DATE)
