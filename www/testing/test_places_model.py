#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, rainbow_place, wild_place, knights_of_the_round_table, RAINBOW_PLACE_NAME, RAINBOW_PLACE_DESCRIPTION, \
    RAINBOW_PLACE_DATE, WILD_PLACE_NAME, WILD_PLACE_DESCRIPTION, WILD_PLACE_DATE


def _pycharm_please_keep_these_imports():
    return app, knights_of_the_round_table, rainbow_place, wild_place


def test_place_creation(knights_of_the_round_table, rainbow_place, wild_place):
    assert rainbow_place != wild_place

    assert rainbow_place.name == RAINBOW_PLACE_NAME
    assert rainbow_place.description == RAINBOW_PLACE_DESCRIPTION
    assert rainbow_place.date_created == RAINBOW_PLACE_DATE
    assert rainbow_place.place_of == knights_of_the_round_table.place

    assert wild_place.name == WILD_PLACE_NAME
    assert wild_place.description == WILD_PLACE_DESCRIPTION
    assert wild_place.date_created == WILD_PLACE_DATE
    assert wild_place.place_of == knights_of_the_round_table.place

