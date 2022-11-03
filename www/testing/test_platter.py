#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, rainbow_place, wild_place, light_saber, muffin, roll, pastry, \
    knights_of_the_round_table, queens_of_the_round_table
from tracking.navigation.platter import Platter, PlatterById


def _pycharm_please_keep_these_imports():
    return app, rainbow_place, wild_place, light_saber, muffin, roll, pastry, knights_of_the_round_table, \
           queens_of_the_round_table


def test_construction(app, knights_of_the_round_table, rainbow_place, light_saber, muffin, roll):
    specification = knights_of_the_round_table.find_or_create_specification({muffin, roll})

    place_only_platter = Platter(place=rainbow_place)
    assert place_only_platter.root == knights_of_the_round_table
    assert place_only_platter.place == rainbow_place
    assert place_only_platter.thing == knights_of_the_round_table.thing
    assert place_only_platter.specification == knights_of_the_round_table.generic_specification
    assert place_only_platter.is_valid

    thing_only_platter = Platter(thing=light_saber)
    assert thing_only_platter.root == knights_of_the_round_table
    assert thing_only_platter.place == knights_of_the_round_table.place
    assert thing_only_platter.thing == light_saber
    assert thing_only_platter.specification == knights_of_the_round_table.generic_specification
    assert place_only_platter.is_valid

    specification_only_platter = Platter(specification=specification)
    assert specification_only_platter.root == knights_of_the_round_table
    assert specification_only_platter.place == knights_of_the_round_table.place
    assert specification_only_platter.thing == specification_only_platter.thing
    assert specification_only_platter.specification == specification
    assert thing_only_platter.is_valid

    root_only_platter = Platter(root=knights_of_the_round_table)
    assert root_only_platter.root == knights_of_the_round_table
    assert root_only_platter.place == knights_of_the_round_table.place
    assert root_only_platter.thing == specification_only_platter.thing
    assert root_only_platter.specification == knights_of_the_round_table.generic_specification
    assert root_only_platter.is_valid

    empty_platter = Platter()
    assert empty_platter.root is None
    assert empty_platter.place is None
    assert empty_platter.thing is None
    assert empty_platter.specification is None
    assert not empty_platter.is_valid


def test_bad_construction(app, queens_of_the_round_table, knights_of_the_round_table, rainbow_place):
    assert not Platter(root=queens_of_the_round_table, place=rainbow_place).is_valid


def test_create_platter(app, knights_of_the_round_table, rainbow_place, light_saber, muffin, roll):
    specification = knights_of_the_round_table.find_or_create_specification({muffin, roll})
    platter = PlatterById(root_id=knights_of_the_round_table.id, place_id=rainbow_place.id,
                          thing_id=light_saber.id, specification_id=specification.id)
    assert platter is not None
    assert platter.root == knights_of_the_round_table
    assert platter.place == rainbow_place
    assert platter.thing == light_saber
    assert platter.specification == specification
