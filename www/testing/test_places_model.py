#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures_for_testing import app, knights_of_the_round_table, rainbow_place, PLACE_NAME, PLACE_DESCRIPTION, \
    PLACE_DATE


def _pycharm_please_keep_these_imports():
    return app, knights_of_the_round_table, rainbow_place


def test_place_creation(knights_of_the_round_table, rainbow_place):
    assert rainbow_place.name == PLACE_NAME
    assert rainbow_place.description == PLACE_DESCRIPTION
    assert rainbow_place.date_created == PLACE_DATE
    assert rainbow_place.group == knights_of_the_round_table
