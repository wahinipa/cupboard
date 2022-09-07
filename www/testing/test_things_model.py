#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures_for_testing import app, light_saber, LIGHT_SABER_THING_NAME, LIGHT_SABER_THING_DESCRIPTION, \
    LIGHT_SABER_THING_DATE
from tracking.things.thing_models import find_or_create_thing


def _pycharm_please_keep_these_imports():
    return app, light_saber


def test_thing_creation(light_saber):
    assert light_saber.name == LIGHT_SABER_THING_NAME
    assert light_saber.description == LIGHT_SABER_THING_DESCRIPTION
    assert light_saber.date_created == LIGHT_SABER_THING_DATE
    kind = light_saber.kind_of
    assert kind is not None
    assert kind.name == "Everything"
    assert light_saber in kind.kinds


def test_things_are_unique_by_name(light_saber):
    thing = find_or_create_thing(LIGHT_SABER_THING_NAME, LIGHT_SABER_THING_DESCRIPTION)
    assert thing is not None
    assert thing == light_saber
