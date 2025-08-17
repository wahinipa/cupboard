#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime
from os import environ, path, remove

import pytest

from flask import current_app, Flask
from tracking import create_app, database
from tracking.modelling.choice_model import find_or_create_choice
from tracking.modelling.role_models import find_or_create_role
from tracking.modelling.root_model import create_root
from tracking.modelling.people_model import find_or_create_user


#############################
# Application Test Fixtures #
#############################


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        # if environ.get('TEST_SQL_IN_MEMORY') != 'True':
        #     basedir = path.abspath(path.dirname(__file__))
        #     test_data_base = path.join(basedir, 'cupboard_test.db')
        #     yield app
        #     remove(test_data_base)
        # else:
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


ROUND_TABLE_DATE = datetime(1994, 6, 12)

QUEENS_TABLE_GROUP_NAME = "Queens of the Square Table"
QUEENS_TABLE_DESCRIPTION = "Bunch of Snoots"
QUEENS_TABLE_DATE = datetime(1993, 5, 10)

# @pytest.fixture()
def knights_of_the_round_table(app):
    return create_root(name=ROOT_NAME, description=ROOT_DESCRIPTION, date_created=ROUND_TABLE_DATE)


@pytest.fixture()
def queens_of_the_round_table(app):
    return create_root(name=QUEENS_TABLE_GROUP_NAME, description=QUEENS_TABLE_DESCRIPTION, date_created=QUEENS_TABLE_DATE)


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
def light_saber(app, knights_of_the_round_table):
    return knights_of_the_round_table.thing.create_kind_of_thing(name=LIGHT_SABER_THING_NAME, description=LIGHT_SABER_THING_DESCRIPTION,
                                               date_created=LIGHT_SABER_THING_DATE)


BUCKET_NAME = "Bucket"
BUCKET_DESCRIPTION = "Useful for hauling water."
BUCKET_DATE = datetime(1981, 5, 4)


@pytest.fixture()
def bucket(app, knights_of_the_round_table):
    return knights_of_the_round_table.thing.create_kind_of_thing(BUCKET_NAME, BUCKET_DESCRIPTION, date_created=BUCKET_DATE)


SHARP_SABER_THING_NAME = "Sharp Light Saber"
SHARP_SABER_THING_DESCRIPTION = "Useful for mostly defeating galactic tyranny."
SHARP_SABER_THING_DATE = datetime(1984, 2, 3)


@pytest.fixture()
def sharp_saber(app, light_saber):
    return light_saber.create_kind_of_thing(name=SHARP_SABER_THING_NAME, description=SHARP_SABER_THING_DESCRIPTION,
                                            date_created=SHARP_SABER_THING_DATE)


DULL_SABER_THING_NAME = "Dull Light Saber"
DULL_SABER_THING_DESCRIPTION = "Useful for barely defeating galactic tyranny."
DULL_SABER_THING_DATE = datetime(1984, 12, 3)


@pytest.fixture()
def dull_saber(app, light_saber):
    return light_saber.create_kind_of_thing(name=DULL_SABER_THING_NAME, description=DULL_SABER_THING_DESCRIPTION,
                                            date_created=DULL_SABER_THING_DATE)


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
    return knights_of_the_round_table.place.create_kind_of_place(RAINBOW_PLACE_NAME, RAINBOW_PLACE_DESCRIPTION,
                                               date_created=RAINBOW_PLACE_DATE)


@pytest.fixture()
def wild_place(app, knights_of_the_round_table):
    return knights_of_the_round_table.place.create_kind_of_place(WILD_PLACE_NAME, WILD_PLACE_DESCRIPTION,
                                               date_created=WILD_PLACE_DATE)


##########################
# Category Test Fixtures #
##########################


PASTRY_NAME = "pastry"
PASTRY_DESCRIPTION = "Yummy!"
PASTRY_DATE = datetime(1989, 12, 13)


@pytest.fixture()
def pastry(app, knights_of_the_round_table):
    return knights_of_the_round_table.create_category(PASTRY_NAME, description=PASTRY_DESCRIPTION, date_created=PASTRY_DATE)


COLORING_NAME = "coloring"
COLORING_DESCRIPTION = "hue and all that"
COLORING_DATE = datetime(1979, 2, 17)


@pytest.fixture()
def coloring(app, knights_of_the_round_table):
    return knights_of_the_round_table.create_category(COLORING_NAME, description=COLORING_DESCRIPTION, date_created=COLORING_DATE)


########################
# Choice Test Fixtures #
########################

MUFFIN_NAME = "Muffin"
MUFFIN_DESCRIPTION = "Blueberry"
MUFFIN_DATE = datetime(1988, 11, 15)

ROLL_NAME = "Roll"
ROLL_DESCRIPTION = "Cinnamon"
ROLL_DATE = datetime(1987, 10, 14)

RED_COLORING_NAME = "Red"
RED_COLORING_DESCRIPTION = "Dark Pink"
RED_COLORING_DATE = datetime(1957, 11, 13)


@pytest.fixture()
def muffin(app, pastry, knights_of_the_round_table):
    return find_or_create_choice(pastry, MUFFIN_NAME, description=MUFFIN_DESCRIPTION, date_created=MUFFIN_DATE)


@pytest.fixture()
def roll(app, pastry, knights_of_the_round_table):
    return find_or_create_choice(pastry, ROLL_NAME, description=ROLL_DESCRIPTION, date_created=ROLL_DATE)


@pytest.fixture()
def blue_coloring(app, coloring, knights_of_the_round_table):
    return find_or_create_choice(coloring, "Blue Coloring", description="It is blue",
                                 date_created=RED_COLORING_DATE)

@pytest.fixture()
def red_coloring(app, coloring, knights_of_the_round_table):
    return find_or_create_choice(coloring, RED_COLORING_NAME, description=RED_COLORING_DESCRIPTION,
                                 date_created=RED_COLORING_DATE)


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
    return find_or_create_role(DUNCE_ROLE_NAME, DUNCE_DESCRIPTION, DUNCE_DATE)


@pytest.fixture()
def buffoon(app):
    return find_or_create_role(BUFFOON_ROLE_NAME, BUFFOON_DESCRIPTION, BUFFOON_DATE)


@pytest.fixture()
def bossy(app):
    return find_or_create_role(BOSSY_ROLE_NAME, BOSSY_DESCRIPTION, BOSSY_DATE)
