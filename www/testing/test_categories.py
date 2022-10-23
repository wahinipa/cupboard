#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, light_saber, pastry, coloring, PASTRY_NAME, PASTRY_DESCRIPTION, PASTRY_DATE, \
    COLORING_NAME, COLORING_DESCRIPTION, COLORING_DATE, knights_of_the_round_table, sharp_saber, dull_saber


def _pycharm_please_keep_these_imports():
    return app, pastry, light_saber, coloring, knights_of_the_round_table, sharp_saber, dull_saber


def test_category_creation(knights_of_the_round_table, pastry, coloring):
    assert pastry is not None
    assert pastry.name == PASTRY_NAME
    assert pastry.description == PASTRY_DESCRIPTION
    assert pastry.date_created == PASTRY_DATE
    assert pastry.root == knights_of_the_round_table

    assert coloring is not None
    assert coloring.name == COLORING_NAME
    assert coloring.description == COLORING_DESCRIPTION
    assert coloring.date_created == COLORING_DATE
    assert coloring.root == knights_of_the_round_table
