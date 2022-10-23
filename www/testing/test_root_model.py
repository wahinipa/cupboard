#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, knights_of_the_round_table, ROOT_NAME, ROOT_DESCRIPTION


def _pycharm_please_keep_these_imports():
    return app, knights_of_the_round_table


def test_root_creation(knights_of_the_round_table):
    assert knights_of_the_round_table is not None
    assert knights_of_the_round_table.name == ROOT_NAME
    assert knights_of_the_round_table.description == ROOT_DESCRIPTION

    top_place = knights_of_the_round_table.place
    assert top_place is not None
    assert top_place.root == knights_of_the_round_table
    assert top_place.name == 'Everywhere'

    top_thing = knights_of_the_round_table.thing
    assert top_thing is not None
    assert top_thing.root == knights_of_the_round_table
    assert top_thing.name == 'Everything'
