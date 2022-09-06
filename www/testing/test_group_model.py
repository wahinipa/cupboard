#  Copyright (c) 2022, Wahinipa LLC

from testing.fixtures_for_testing import app, knights_of_the_round_table, ROUND_TABLE_GROUP_NAME, \
    ROUND_TABLE_DESCRIPTION, ROUND_TABLE_DATE, queens_of_the_round_table, QUEENS_TABLE_GROUP_NAME, QUEENS_TABLE_DATE, \
    QUEENS_TABLE_DESCRIPTION


def _pycharm_please_keep_these_imports():
    return app, knights_of_the_round_table, queens_of_the_round_table


def test_group_creation(knights_of_the_round_table, queens_of_the_round_table):
    assert knights_of_the_round_table.name == ROUND_TABLE_GROUP_NAME
    assert knights_of_the_round_table.description == ROUND_TABLE_DESCRIPTION
    assert knights_of_the_round_table.date_created == ROUND_TABLE_DATE

    assert queens_of_the_round_table.name == QUEENS_TABLE_GROUP_NAME
    assert queens_of_the_round_table.description == QUEENS_TABLE_DESCRIPTION
    assert queens_of_the_round_table.date_created == QUEENS_TABLE_DATE
