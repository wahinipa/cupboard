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
    blue_muffin_choice_set = {muffin, blue_coloring}
    blue_muffin_specification = knights_of_the_round_table.find_or_create_specification(choices=blue_muffin_choice_set)
    assert blue_muffin_specification is not None
    assert blue_muffin_specification.root == knights_of_the_round_table

    specifics = blue_muffin_specification.specifics
    assert specifics is not None
    assert len(specifics) == 2

    choices = blue_muffin_specification.choices
    assert choices is not None
    assert len(choices) == 2
    assert choices == blue_muffin_choice_set

    assert blue_muffin_specification.has_choice(muffin)
    assert blue_muffin_specification.has_choice(blue_coloring)
    assert not blue_muffin_specification.has_choice(roll)
    assert not blue_muffin_specification.has_choice(red_coloring)

    found_specification = knights_of_the_round_table.find_specification(choices=blue_muffin_choice_set)
    assert found_specification is not None
    assert found_specification == blue_muffin_specification

    no_such_specification = knights_of_the_round_table.find_specification(choices={muffin, red_coloring})
    assert no_such_specification is None

    another_specification = knights_of_the_round_table.find_or_create_specification(choices=blue_muffin_choice_set)
    assert another_specification is not None
    assert blue_muffin_specification == another_specification


def test_listed_choice_specification(app, knights_of_the_round_table, pastry, coloring, muffin, roll, red_coloring,
                                     blue_coloring):
    specification = knights_of_the_round_table.find_or_create_specification(choices={muffin, blue_coloring})
    assert specification is not None

    specification == knights_of_the_round_table.find_or_create_specification(choices=[muffin, blue_coloring])

    def listing():
        for choice in [blue_coloring, muffin]:
            yield choice

    specification == knights_of_the_round_table.find_or_create_specification(choices=listing())


def test_categories_in_specification(app, knights_of_the_round_table, pastry, coloring, muffin, roll, red_coloring,
                                     blue_coloring):
    blue_muffin_specification = knights_of_the_round_table.find_or_create_specification(choices={muffin, blue_coloring})
    muffin_roll_specification = knights_of_the_round_table.find_or_create_specification(choices={muffin, roll})
    generic_specification = knights_of_the_round_table.generic_specification

    assert not generic_specification.choices_for(pastry)
    assert not generic_specification.choices_for(coloring)

    assert blue_muffin_specification.choices_for(pastry) == {muffin}
    assert blue_muffin_specification.choices_for(coloring) == {blue_coloring}

    assert muffin_roll_specification.choices_for(pastry) == {muffin, roll}
    assert not muffin_roll_specification.choices_for(coloring)


def test_unknown_specification(app, knights_of_the_round_table, pastry, coloring, muffin, roll, red_coloring,
                               blue_coloring):
    blue_unknown_pastry_specification = knights_of_the_round_table.find_or_create_specification(
        choices={blue_coloring},
        unknowns={pastry}
    )
    assert blue_unknown_pastry_specification is not None
    assert not blue_unknown_pastry_specification.choices_for(pastry)
    assert blue_unknown_pastry_specification.choices_for(coloring) == {blue_coloring}
    retrieved_unknowns = blue_unknown_pastry_specification.unknowns
    assert retrieved_unknowns == {pastry}


def test_specification_matching(app, knights_of_the_round_table, pastry, coloring, muffin, roll, red_coloring,
                                blue_coloring):
    # All the different target specifications
    generic_specification = knights_of_the_round_table.generic_specification
    blue_specification = knights_of_the_round_table.find_or_create_specification(choices={blue_coloring})
    red_specification = knights_of_the_round_table.find_or_create_specification(choices={red_coloring})
    muffin_specification = knights_of_the_round_table.find_or_create_specification(choices={muffin})
    roll_specification = knights_of_the_round_table.find_or_create_specification(choices={roll})
    blue_muffin_specification = knights_of_the_round_table.find_or_create_specification(choices={muffin, blue_coloring})
    red_muffin_specification = knights_of_the_round_table.find_or_create_specification(choices={muffin, red_coloring})
    blue_roll_specification = knights_of_the_round_table.find_or_create_specification(choices={roll, blue_coloring})
    red_roll_specification = knights_of_the_round_table.find_or_create_specification(choices={roll, red_coloring})

    # Additional search specifications
    muffin_roll_specification = knights_of_the_round_table.find_or_create_specification(choices={muffin, roll})
    red_blue_specification = knights_of_the_round_table.find_or_create_specification(
        choices={red_coloring, blue_coloring})
    red_muffin_roll_specification = knights_of_the_round_table.find_or_create_specification(
        choices={red_coloring, muffin, roll})
    red_blue_roll_specification = knights_of_the_round_table.find_or_create_specification(
        choices={red_coloring, blue_coloring, roll})
    muffins_of_unknown_color_specification = knights_of_the_round_table.find_or_create_specification(
        choices={muffin}, unknowns={coloring})
    muffins_of_red_or_unknown_color_specification = knights_of_the_round_table.find_or_create_specification(
        choices={muffin, red_coloring}, unknowns={coloring})

    exact_specifications = [blue_muffin_specification, red_muffin_specification, blue_roll_specification,
                            red_roll_specification]
    inexact_targets = [generic_specification, blue_specification, red_specification, muffin_specification,
                       roll_specification]
    for search in exact_specifications:
        for target in exact_specifications:
            # Accept only exact matches
            if target == search:
                assert search.accepts(target)
            else:
                assert not search.accepts(target)
        # Reject all inexact targets
        for target in inexact_targets:
            assert not search.accepts(target)

    # accept anything blue
    for target in [blue_muffin_specification, blue_roll_specification, blue_specification]:
        assert blue_specification.accepts(target)

    # reject anything not blue
    for target in [red_muffin_specification, red_roll_specification, red_specification, generic_specification,
                   muffin_specification, roll_specification]:
        assert not blue_specification.accepts(target)

    assert not muffins_of_unknown_color_specification.accepts(blue_muffin_specification)
    assert muffins_of_red_or_unknown_color_specification.accepts(red_muffin_specification)
    for target in exact_specifications + inexact_targets:
        if target == muffin_specification:
            assert muffins_of_unknown_color_specification.accepts(target)
        else:
            acceptance = muffins_of_unknown_color_specification.accepts(target)
            if acceptance:
                assert False
        is_red_muffin = red_muffin_specification.accepts(target)
        is_muffin_of_unknown_color = muffins_of_unknown_color_specification.accepts(target)
        if muffins_of_red_or_unknown_color_specification.accepts(target):
            assert is_red_muffin or is_muffin_of_unknown_color
        else:
            assert not is_red_muffin or not is_muffin_of_unknown_color
