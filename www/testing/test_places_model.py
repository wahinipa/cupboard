#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, rainbow_place, wild_place, knights_of_the_round_table, RAINBOW_PLACE_NAME, \
    RAINBOW_PLACE_DESCRIPTION, \
    RAINBOW_PLACE_DATE, WILD_PLACE_NAME, WILD_PLACE_DESCRIPTION, WILD_PLACE_DATE


def _pycharm_please_keep_these_imports():
    return app, knights_of_the_round_table, rainbow_place, wild_place


def test_place_creation(knights_of_the_round_table, rainbow_place, wild_place):
    top_place = knights_of_the_round_table.place
    assert top_place.root == knights_of_the_round_table

    assert rainbow_place != wild_place
    assert rainbow_place.root == knights_of_the_round_table

    assert rainbow_place.name == RAINBOW_PLACE_NAME
    assert rainbow_place.description == RAINBOW_PLACE_DESCRIPTION
    assert rainbow_place.date_created == RAINBOW_PLACE_DATE
    assert rainbow_place.place_of == knights_of_the_round_table.place

    assert wild_place.name == WILD_PLACE_NAME
    assert wild_place.description == WILD_PLACE_DESCRIPTION
    assert wild_place.date_created == WILD_PLACE_DATE
    assert wild_place.place_of == knights_of_the_round_table.place
    assert wild_place.root == knights_of_the_round_table

    rainbow_inner_1 = rainbow_place.create_kind_of_place('aaa', 'bbb')
    assert rainbow_inner_1.root == knights_of_the_round_table

    rainbow_inner_2 = rainbow_place.create_kind_of_place('ccc', 'ddd')
    assert rainbow_inner_2.root == knights_of_the_round_table

    rainbow_inner_11 = rainbow_inner_1.create_kind_of_place('eee', 'fff')
    assert rainbow_inner_11.root == knights_of_the_round_table

    assert len(top_place.domain) == 5
    assert len(top_place.complete_domain) == 6

    assert len(wild_place.domain) == 0
    assert len(wild_place.complete_domain) == 1

    assert len(rainbow_inner_11.domain) == 0
    assert len(rainbow_inner_11.complete_domain) == 1

    assert len(rainbow_place.domain) == 3
    assert len(rainbow_place.complete_domain) == 4

    assert len(rainbow_inner_1.domain) == 1
    assert len(rainbow_inner_1.complete_domain) == 2

    assert len(rainbow_inner_2.domain) == 0
    assert len(rainbow_inner_2.complete_domain) == 1

    assert len(rainbow_inner_11.domain) == 0
    assert len(rainbow_inner_11.complete_domain) == 1

