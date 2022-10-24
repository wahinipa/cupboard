#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, muffin, roll, blue_coloring, red_coloring, knights_of_the_round_table, pastry, \
    coloring


def _pycharm_please_keep_these_imports():
    return app, knights_of_the_round_table, pastry, coloring, muffin, roll, blue_coloring, red_coloring


def test_generic_specification(app, knights_of_the_round_table):
    generic = knights_of_the_round_table.find_or_create_specification()
    assert generic is not None
    assert generic.root == knights_of_the_round_table

    specifics = generic.specifics
    assert specifics is not None
    assert len(specifics) == 0

    choices = generic.choices
    assert choices is not None
    assert len(choices) == 0


def test_busy_specification(app, knights_of_the_round_table, pastry, coloring, muffin, roll, red_coloring,
                            blue_coloring):
    specification = knights_of_the_round_table.find_or_create_specification(choices={muffin, blue_coloring})
    assert specification is not None
    assert specification.root == knights_of_the_round_table

    specifics = specification.specifics
    assert specifics is not None
    assert len(specifics) == 2

    choices = specification.choices
    assert choices is not None
    assert len(choices) == 2

    assert specification.has_choice(muffin)
    assert specification.has_choice(blue_coloring)
    assert not specification.has_choice(roll)
    assert not specification.has_choice(red_coloring)

    found_specification = knights_of_the_round_table.find_specification(choices={muffin, blue_coloring})
    assert found_specification is not None
    assert found_specification == specification

    no_such_specification = knights_of_the_round_table.find_specification(choices={muffin, red_coloring})
    assert no_such_specification is None

    another_specification = knights_of_the_round_table.find_or_create_specification(choices={muffin, blue_coloring})
    assert another_specification is not None
    assert specification == another_specification


def test_listed_choice_specification(app, knights_of_the_round_table, pastry, coloring, muffin, roll, red_coloring,
                                     blue_coloring):
    specification = knights_of_the_round_table.find_or_create_specification(choices={muffin, blue_coloring})
    assert specification is not None

    specification == knights_of_the_round_table.find_or_create_specification(choices=[muffin, blue_coloring])

    def listing():
        for choice in [blue_coloring, muffin]:
            yield choice

    specification == knights_of_the_round_table.find_or_create_specification(choices=listing())
