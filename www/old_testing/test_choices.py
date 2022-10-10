#  Copyright (c) 2022, Wahinipa LLC
from old_testing.fixtures_for_testing import RED_COLORING_DATE, RED_COLORING_DESCRIPTION, RED_COLORING_NAME, app, pastry, \
    muffin, roll, \
    red_coloring, coloring, \
    MUFFIN_NAME, MUFFIN_DESCRIPTION, MUFFIN_DATE, \
    ROLL_NAME, ROLL_DESCRIPTION, ROLL_DATE
from tracking.choices.choice_models import find_or_create_choice


def _pycharm_please_keep_these_imports():
    return app, pastry, muffin, roll, red_coloring, coloring


def test_choice_creation(pastry, muffin, roll, red_coloring, coloring):
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

    assert red_coloring is not None
    assert red_coloring.name == RED_COLORING_NAME
    assert red_coloring.description == RED_COLORING_DESCRIPTION
    assert red_coloring.date_created == RED_COLORING_DATE
    assert red_coloring.category == coloring
    assert red_coloring in coloring.choices


def test_choice_is_unique(pastry, muffin):
    another_muffin = find_or_create_choice(pastry, MUFFIN_NAME, description=MUFFIN_DESCRIPTION,
                                           date_created=MUFFIN_DATE)
    assert muffin == another_muffin
