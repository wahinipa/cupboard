#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, light_saber, pastry, coloring, PASTRY_NAME, PASTRY_DESCRIPTION, PASTRY_DATE, \
    COLORING_NAME, COLORING_DESCRIPTION, COLORING_DATE, the_root, sharp_saber, dull_saber


def _pycharm_please_keep_these_imports():
    return app, pastry, light_saber, coloring, the_root, sharp_saber, dull_saber


def test_category_creation(the_root, pastry, coloring):
    assert pastry is not None
    assert pastry.name == PASTRY_NAME
    assert pastry.description == PASTRY_DESCRIPTION
    assert pastry.date_created == PASTRY_DATE
    assert pastry.root == the_root

    assert coloring is not None
    assert coloring.name == COLORING_NAME
    assert coloring.description == COLORING_DESCRIPTION
    assert coloring.date_created == COLORING_DATE
    assert coloring.root == the_root
