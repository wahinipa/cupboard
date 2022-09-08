#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures_for_testing import app, pastry, muffin, MUFFIN_NAME, MUFFIN_DESCRIPTION, MUFFIN_DATE


def _pycharm_please_keep_these_imports():
    return app, pastry, muffin


def test_category_creation(pastry, muffin):
    assert muffin is not None
    assert muffin.name == MUFFIN_NAME
    assert muffin.description == MUFFIN_DESCRIPTION
    assert muffin.date_created == MUFFIN_DATE
    assert muffin.category == pastry
    assert muffin in pastry.choices
