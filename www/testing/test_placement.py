#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, rainbow_place, wild_place, light_saber, muffin, roll, pastry, \
    knights_of_the_round_table, queens_of_the_round_table
from tracking.modelling.placement_model import Placement, create_placement


def _pycharm_please_keep_these_imports():
    return app, rainbow_place, wild_place, light_saber, muffin, roll, pastry, knights_of_the_round_table, \
           queens_of_the_round_table


def test_construction(app, knights_of_the_round_table, rainbow_place, light_saber, muffin, roll):
    specification = knights_of_the_round_table.find_or_create_specification({muffin, roll})

    place_only_placement = Placement(place=rainbow_place)
    assert place_only_placement.root == knights_of_the_round_table
    assert place_only_placement.place == rainbow_place
    assert place_only_placement.thing == knights_of_the_round_table.thing
    assert place_only_placement.specification == knights_of_the_round_table.generic_specification
    assert place_only_placement.is_valid

    thing_only_placement = Placement(thing=light_saber)
    assert thing_only_placement.root == knights_of_the_round_table
    assert thing_only_placement.place == knights_of_the_round_table.place
    assert thing_only_placement.thing == light_saber
    assert thing_only_placement.specification == knights_of_the_round_table.generic_specification
    assert place_only_placement.is_valid

    specification_only_placement = Placement(specification=specification)
    assert specification_only_placement.root == knights_of_the_round_table
    assert specification_only_placement.place == knights_of_the_round_table.place
    assert specification_only_placement.thing == specification_only_placement.thing
    assert specification_only_placement.specification == specification
    assert thing_only_placement.is_valid

    root_only_placement = Placement(root=knights_of_the_round_table)
    assert root_only_placement.root == knights_of_the_round_table
    assert root_only_placement.place == knights_of_the_round_table.place
    assert root_only_placement.thing == specification_only_placement.thing
    assert root_only_placement.specification == knights_of_the_round_table.generic_specification
    assert root_only_placement.is_valid

    empty_placement = Placement()
    assert empty_placement.root is None
    assert empty_placement.place is None
    assert empty_placement.thing is None
    assert empty_placement.specification is None
    assert not empty_placement.is_valid


def test_bad_construction(app, queens_of_the_round_table, knights_of_the_round_table, rainbow_place):
    assert not Placement(root=queens_of_the_round_table, place=rainbow_place).is_valid


def test_create_placement(app, knights_of_the_round_table, rainbow_place, light_saber, muffin, roll):
    specification = knights_of_the_round_table.find_or_create_specification({muffin, roll})
    placement = create_placement(root_id=knights_of_the_round_table.id, place_id=rainbow_place.id,
                                 thing_id=light_saber.id, specification_id=specification.id)
    assert placement is not None
    assert placement.root == knights_of_the_round_table
    assert placement.place == rainbow_place
    assert placement.thing == light_saber
    assert placement.specification == specification
