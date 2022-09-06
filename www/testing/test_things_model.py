#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures_for_testing import app, light_saber, THING_NAME, THING_DESCRIPTION, THING_DATE


def _pycharm_please_keep_these_imports():
    return app, light_saber


def test_thing_creation(light_saber):
    assert light_saber.name == THING_NAME
    assert light_saber.description == THING_DESCRIPTION
    assert light_saber.date_created == THING_DATE
