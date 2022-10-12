#  Copyright (c) 2022, Wahinipa LLC
from old_testing.fixtures_for_testing import RAINBOW_PLACE_DATE, RAINBOW_PLACE_DESCRIPTION, RAINBOW_PLACE_NAME, \
    WILD_PLACE_DATE, WILD_PLACE_DESCRIPTION, WILD_PLACE_NAME, app, knights_of_the_round_table, \
    queens_of_the_round_table, rainbow_place, wild_place
from tracking.places.old_place_models import find_or_create_place


def _pycharm_please_keep_these_imports():
    return app, knights_of_the_round_table, queens_of_the_round_table, rainbow_place, wild_place


def test_place_creation(knights_of_the_round_table, rainbow_place, wild_place):
    assert rainbow_place != wild_place

    assert rainbow_place.name == RAINBOW_PLACE_NAME
    assert rainbow_place.description == RAINBOW_PLACE_DESCRIPTION
    assert rainbow_place.date_created == RAINBOW_PLACE_DATE
    assert rainbow_place.group == knights_of_the_round_table

    assert wild_place.name == WILD_PLACE_NAME
    assert wild_place.description == WILD_PLACE_DESCRIPTION
    assert wild_place.date_created == WILD_PLACE_DATE
    assert wild_place.group == knights_of_the_round_table


def test_groups_may_have_places_with_same_name(knights_of_the_round_table, queens_of_the_round_table, rainbow_place):
    queens_rainbow_place = find_or_create_place(queens_of_the_round_table, RAINBOW_PLACE_NAME,
                                                RAINBOW_PLACE_DESCRIPTION,
                                                date_created=RAINBOW_PLACE_DATE)
    assert queens_rainbow_place is not None


def test_place_name_unique_within_group(knights_of_the_round_table, queens_of_the_round_table, rainbow_place):
    knights_rainbow_place = find_or_create_place(knights_of_the_round_table, RAINBOW_PLACE_NAME,
                                                 RAINBOW_PLACE_DESCRIPTION,
                                                 date_created=RAINBOW_PLACE_DATE)
    assert knights_rainbow_place is not None
    assert knights_rainbow_place == rainbow_place