#  Copyright (c) 2022. Wahinipa LLC

from testing.fixtures_for_testing import app, knights_of_the_round_table, GROUP_NAME, GROUP_DESCRIPTION, GROUP_DATE


def _pycharm_please_keep_these_imports():
    return app, knights_of_the_round_table


def test_group_creation(knights_of_the_round_table):
    assert knights_of_the_round_table.name == GROUP_NAME
    assert knights_of_the_round_table.description == GROUP_DESCRIPTION
    assert knights_of_the_round_table.date_created == GROUP_DATE
