#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures_for_testing import app, pastry, PASTRY_NAME, PASTRY_DESCRIPTION, PASTRY_DATE


def _pycharm_please_keep_these_imports():
    return app, pastry


def test_category_creation(pastry):
    assert pastry is not None
    assert pastry.name == PASTRY_NAME
    assert pastry.description == PASTRY_DESCRIPTION
    assert pastry.date_created == PASTRY_DATE
