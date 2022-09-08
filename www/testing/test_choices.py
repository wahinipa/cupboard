#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures_for_testing import app, pastry, muffin, roll, MUFFIN_NAME, MUFFIN_DESCRIPTION, MUFFIN_DATE, \
    ROLL_NAME, ROLL_DESCRIPTION, ROLL_DATE


def _pycharm_please_keep_these_imports():
    return app, pastry, muffin, roll


def test_choice_creation(pastry, muffin, roll):
    assert muffin is not None
    assert muffin.name == MUFFIN_NAME
    assert muffin.description == MUFFIN_DESCRIPTION
    assert muffin.date_created == MUFFIN_DATE
    assert muffin.category == pastry
    assert muffin in pastry.choices

    assert roll is not None
    assert roll.name == ROLL_NAME
    assert roll.description == ROLL_DESCRIPTION
    assert roll.date_created == ROLL_DATE
    assert roll.category == pastry
    assert roll in pastry.choices
