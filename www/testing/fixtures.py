#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ, path, remove

import pytest

from tracking import create_app, database
from tracking.modelling.root_model import create_root
from tracking.modelling.people_model import find_or_create_user


#############################
# Application Test Fixtures #
#############################


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


#######################
# Root Test Fixtures #
#######################

ROOT_NAME = "The Root"
ROOT_DESCRIPTION = "Base Testing Object"
ROOT_PLACE_NAME = "All The Root Places"
ROOT_THING_NAME = "All The Root Things"

@pytest.fixture()
def the_root(app):
    return create_root(name=ROOT_NAME, description=ROOT_DESCRIPTION)


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
# Thing Test Fixtures #
#######################

LIGHT_SABER_THING_NAME = "Light Saber"
LIGHT_SABER_THING_DESCRIPTION = "Useful for defeating galactic tyranny."
LIGHT_SABER_THING_DATE = datetime(1984, 1, 1)


@pytest.fixture()
def light_saber(app, the_root):
    return the_root.thing.create_kind_of_thing(name=LIGHT_SABER_THING_NAME, description=LIGHT_SABER_THING_DESCRIPTION,
                                date_created=LIGHT_SABER_THING_DATE)


BUCKET_NAME = "Bucket"
BUCKET_DESCRIPTION = "Useful for hauling water."
BUCKET_DATE = datetime(1981, 5, 4)


@pytest.fixture()
def bucket(app, the_root):
    return the_root.thing.create_kind_of_thing(BUCKET_NAME, BUCKET_DESCRIPTION, date_created=BUCKET_DATE)


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
def rainbow_place(app, the_root):
    return the_root.place.create_kind_of_place(RAINBOW_PLACE_NAME, RAINBOW_PLACE_DESCRIPTION,
                                               date_created=RAINBOW_PLACE_DATE)


@pytest.fixture()
def wild_place(app, the_root):
    return the_root.place.create_kind_of_place(WILD_PLACE_NAME, WILD_PLACE_DESCRIPTION,
                                date_created=WILD_PLACE_DATE)


