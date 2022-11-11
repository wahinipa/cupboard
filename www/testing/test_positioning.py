#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, rainbow_place, wild_place, light_saber, muffin, roll, pastry, \
    knights_of_the_round_table
from tracking import database
from tracking.modelling.postioning_model import find_exact_quantity_of_things_at_place, add_quantity_of_things, \
    _find_positionings, \
    Positioning, move_quantity_of_things
from tracking.viewers.destination import Destination


def _pycharm_please_keep_these_imports():
    return app, rainbow_place, wild_place, light_saber, muffin, roll, pastry, knights_of_the_round_table


def test_quantities(rainbow_place, wild_place, light_saber, knights_of_the_round_table, muffin, roll):
    muffin_specification = knights_of_the_round_table.find_or_create_specification({muffin})
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, muffin_specification) == 0

    assert add_quantity_of_things(rainbow_place, light_saber, muffin_specification, 3) == 3
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, muffin_specification) == 3

    assert add_quantity_of_things(rainbow_place, light_saber, muffin_specification, 4) == 7
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, muffin_specification) == 7

    assert add_quantity_of_things(rainbow_place, light_saber, muffin_specification, -2) == 5
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, muffin_specification) == 5
    assert rainbow_place.quantity_of_things(light_saber, muffin_specification) == 5

    assert rainbow_place.add_to_thing(light_saber, muffin_specification, 10) == 15
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, muffin_specification) == 15
    assert light_saber.add_to_place(rainbow_place, muffin_specification, 9) == 24
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, muffin_specification) == 24
    # assert light_saber.exact_quantity_at_place(rainbow_place, muffin_specification) == 24
    # assert light_saber.generic.overall_quantity_at_place(rainbow_place) == 24
    everything = light_saber.kind_of
    assert everything is not None
    # assert everything.generic.overall_quantity_at_place(rainbow_place) == 0
    # assert everything.generic.overall_quantity_at_domain(rainbow_place) == 0


def test_domain_quantities(rainbow_place, wild_place, light_saber, knights_of_the_round_table, muffin, roll):
    round_table = knights_of_the_round_table.place
    # generic_light_saber = light_saber.generic
    roll_specification = knights_of_the_round_table.find_or_create_specification({roll})
    muffin_specification = knights_of_the_round_table.find_or_create_specification({muffin})
    generic_specification = knights_of_the_round_table.find_or_create_specification(set())
    # # muffin_light_saber = find_or_create_particular_thing(light_saber, {muffin})
    # # roll_light_saber = find_or_create_particular_thing(light_saber, {roll})
    #
    # assert generic_light_saber.exact_quantity_at_place(round_table) == 0
    # assert generic_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_place(wild_place) == 0
    # assert generic_light_saber.exact_quantity_at_domain(round_table) == 0
    # assert generic_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_domain(wild_place) == 0
    # assert generic_light_saber.overall_quantity_at_place(round_table) == 0
    # assert generic_light_saber.overall_quantity_at_place(rainbow_place) == 0
    # assert generic_light_saber.overall_quantity_at_place(wild_place) == 0
    # assert generic_light_saber.overall_quantity_at_domain(round_table) == 0
    # assert generic_light_saber.overall_quantity_at_domain(rainbow_place) == 0
    # assert generic_light_saber.overall_quantity_at_domain(wild_place) == 0
    # assert light_saber.exact_quantity_at_place(round_table, muffin_specification) == 0
    # assert light_saber.exact_quantity_at_place(rainbow_place, muffin_specification) == 0
    # assert light_saber.exact_quantity_at_place(wild_place, muffin_specification) == 0
    # assert light_saber.exact_quantity_at_domain(round_table, muffin_specification) == 0
    # assert light_saber.exact_quantity_at_domain(rainbow_place, muffin_specification) == 0
    # assert light_saber.exact_quantity_at_domain(wild_place, muffin_specification) == 0
    # assert light_saber.overall_quantity_at_place(round_table, muffin_specification) == 0
    # assert light_saber.overall_quantity_at_place(rainbow_place, muffin_specification) == 0
    # assert light_saber.overall_quantity_at_place(wild_place, muffin_specification) == 0
    # assert light_saber.overall_quantity_at_domain(round_table, muffin_specification) == 0
    # assert light_saber.overall_quantity_at_domain(rainbow_place, muffin_specification) == 0
    # assert light_saber.overall_quantity_at_domain(wild_place, muffin_specification) == 0
    # assert light_saber.exact_quantity_at_place(round_table, roll_specification) == 0
    # assert roll_light_saber.exact_quantity_at_place(rainbow_place, roll_specification) == 0
    # assert roll_light_saber.exact_quantity_at_place(wild_place, roll_specification) == 0
    # assert roll_light_saber.exact_quantity_at_domain(round_table, roll_specification) == 0
    # assert roll_light_saber.exact_quantity_at_domain(rainbow_place, roll_specification) == 0
    # assert roll_light_saber.exact_quantity_at_domain(wild_place, roll_specification) == 0
    # assert roll_light_saber.overall_quantity_at_place(round_table, roll_specification) == 0
    # assert roll_light_saber.overall_quantity_at_place(rainbow_place, roll_specification) == 0
    # assert roll_light_saber.overall_quantity_at_place(wild_place, roll_specification) == 0
    # assert roll_light_saber.overall_quantity_at_domain(round_table, roll_specification) == 0
    # assert roll_light_saber.overall_quantity_at_domain(rainbow_place, roll_specification) == 0
    # assert roll_light_saber.overall_quantity_at_domain(wild_place, roll_specification) == 0
    #
    # assert add_quantity_of_things(rainbow_place, light_saber, muffin_specification, 3) == 3
    # assert generic_light_saber.exact_quantity_at_place(round_table) == 0
    # assert generic_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_place(wild_place) == 0
    # assert generic_light_saber.exact_quantity_at_domain(round_table) == 0
    # assert generic_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_domain(wild_place) == 0
    # assert generic_light_saber.overall_quantity_at_place(round_table) == 0
    # assert generic_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_place(wild_place) == 0
    # assert generic_light_saber.overall_quantity_at_domain(round_table) == 3
    # assert generic_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_domain(wild_place) == 0
    # assert muffin_light_saber.exact_quantity_at_place(round_table) == 0
    # assert muffin_light_saber.exact_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.exact_quantity_at_domain(round_table) == 3
    # assert muffin_light_saber.exact_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_domain(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_place(round_table) == 0
    # assert muffin_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_domain(round_table) == 3
    # assert muffin_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_domain(wild_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(round_table) == 0
    # assert roll_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(wild_place) == 0
    # assert roll_light_saber.exact_quantity_at_domain(round_table) == 0
    # assert roll_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_domain(wild_place) == 0
    # assert roll_light_saber.overall_quantity_at_place(round_table) == 0
    # assert roll_light_saber.overall_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_place(wild_place) == 0
    # assert roll_light_saber.overall_quantity_at_domain(round_table) == 0
    # assert roll_light_saber.overall_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_domain(wild_place) == 0
    #
    # assert add_quantity_of_things(wild_place, light_saber, roll_specification, 2) == 2
    # assert generic_light_saber.exact_quantity_at_place(round_table) == 0
    # assert generic_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_place(wild_place) == 0
    # assert generic_light_saber.exact_quantity_at_domain(round_table) == 0
    # assert generic_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_domain(wild_place) == 0
    # assert generic_light_saber.overall_quantity_at_place(round_table) == 0
    # assert generic_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_place(wild_place) == 2
    # assert generic_light_saber.overall_quantity_at_domain(round_table) == 5
    # assert generic_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_domain(wild_place) == 2
    # assert muffin_light_saber.exact_quantity_at_place(round_table) == 0
    # assert muffin_light_saber.exact_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.exact_quantity_at_domain(round_table) == 3
    # assert muffin_light_saber.exact_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_domain(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_place(round_table) == 0
    # assert muffin_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_domain(round_table) == 3
    # assert muffin_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_domain(wild_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(round_table) == 0
    # assert roll_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(wild_place) == 2
    # assert roll_light_saber.exact_quantity_at_domain(round_table) == 2
    # assert roll_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_domain(wild_place) == 2
    # assert roll_light_saber.overall_quantity_at_place(round_table) == 0
    # assert roll_light_saber.overall_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_place(wild_place) == 2
    # assert roll_light_saber.overall_quantity_at_domain(round_table) == 2
    # assert roll_light_saber.overall_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_domain(wild_place) == 2
    #
    # assert add_quantity_of_things(wild_place, light_saber, generic_specification, 6) == 6
    # assert add_quantity_of_things(wild_place, light_saber, generic_specification, 4) == 10
    # assert generic_light_saber.exact_quantity_at_place(round_table) == 0
    # assert generic_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_place(wild_place) == 10
    # assert generic_light_saber.exact_quantity_at_domain(round_table) == 10
    # assert generic_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_domain(wild_place) == 10
    # assert generic_light_saber.overall_quantity_at_place(round_table) == 0
    # assert generic_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_place(wild_place) == 12
    # assert generic_light_saber.overall_quantity_at_domain(round_table) == 15
    # assert generic_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_domain(wild_place) == 12
    # assert muffin_light_saber.exact_quantity_at_place(round_table) == 0
    # assert muffin_light_saber.exact_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.exact_quantity_at_domain(round_table) == 3
    # assert muffin_light_saber.exact_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_domain(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_place(round_table) == 0
    # assert muffin_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_domain(round_table) == 3
    # assert muffin_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_domain(wild_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(round_table) == 0
    # assert roll_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(wild_place) == 2
    # assert roll_light_saber.exact_quantity_at_domain(round_table) == 2
    # assert roll_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_domain(wild_place) == 2
    # assert roll_light_saber.overall_quantity_at_place(round_table) == 0
    # assert roll_light_saber.overall_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_place(wild_place) == 2
    # assert roll_light_saber.overall_quantity_at_domain(round_table) == 2
    # assert roll_light_saber.overall_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_domain(wild_place) == 2
    #
    # assert add_quantity_of_things(round_table, light_saber, muffin_specification, 100) == 100
    # assert generic_light_saber.exact_quantity_at_place(round_table) == 0
    # assert generic_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_place(wild_place) == 10
    # assert generic_light_saber.exact_quantity_at_domain(round_table) == 10
    # assert generic_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_domain(wild_place) == 10
    # assert generic_light_saber.overall_quantity_at_place(round_table) == 100
    # assert generic_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_place(wild_place) == 12
    # assert generic_light_saber.overall_quantity_at_domain(round_table) == 115
    # assert generic_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_domain(wild_place) == 12
    # assert muffin_light_saber.exact_quantity_at_place(round_table) == 100
    # assert muffin_light_saber.exact_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.exact_quantity_at_domain(round_table) == 103
    # assert muffin_light_saber.exact_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_domain(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_place(round_table) == 100
    # assert muffin_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_domain(round_table) == 103
    # assert muffin_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_domain(wild_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(round_table) == 0
    # assert roll_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(wild_place) == 2
    # assert roll_light_saber.exact_quantity_at_domain(round_table) == 2
    # assert roll_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_domain(wild_place) == 2
    # assert roll_light_saber.overall_quantity_at_place(round_table) == 0
    # assert roll_light_saber.overall_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_place(wild_place) == 2
    # assert roll_light_saber.overall_quantity_at_domain(round_table) == 2
    # assert roll_light_saber.overall_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_domain(wild_place) == 2
    #
    # assert add_quantity_of_things(round_table, light_saber, generic_specification, 1000) == 1000
    # assert generic_light_saber.exact_quantity_at_place(round_table) == 1000
    # assert generic_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_place(wild_place) == 10
    # assert generic_light_saber.exact_quantity_at_domain(round_table) == 1010
    # assert generic_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert generic_light_saber.exact_quantity_at_domain(wild_place) == 10
    # assert generic_light_saber.overall_quantity_at_place(round_table) == 1100
    # assert generic_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_place(wild_place) == 12
    # assert generic_light_saber.overall_quantity_at_domain(round_table) == 1115
    # assert generic_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert generic_light_saber.overall_quantity_at_domain(wild_place) == 12
    # assert muffin_light_saber.exact_quantity_at_place(round_table) == 100
    # assert muffin_light_saber.exact_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.exact_quantity_at_domain(round_table) == 103
    # assert muffin_light_saber.exact_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.exact_quantity_at_domain(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_place(round_table) == 100
    # assert muffin_light_saber.overall_quantity_at_place(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_place(wild_place) == 0
    # assert muffin_light_saber.overall_quantity_at_domain(round_table) == 103
    # assert muffin_light_saber.overall_quantity_at_domain(rainbow_place) == 3
    # assert muffin_light_saber.overall_quantity_at_domain(wild_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(round_table) == 0
    # assert roll_light_saber.exact_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_place(wild_place) == 2
    # assert roll_light_saber.exact_quantity_at_domain(round_table) == 2
    # assert roll_light_saber.exact_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.exact_quantity_at_domain(wild_place) == 2
    # assert roll_light_saber.overall_quantity_at_place(round_table) == 0
    # assert roll_light_saber.overall_quantity_at_place(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_place(wild_place) == 2
    # assert roll_light_saber.overall_quantity_at_domain(round_table) == 2
    # assert roll_light_saber.overall_quantity_at_domain(rainbow_place) == 0
    # assert roll_light_saber.overall_quantity_at_domain(wild_place) == 2


def test_handles_redundant_quantities(rainbow_place, light_saber, roll, knights_of_the_round_table):
    roll_specification = knights_of_the_round_table.find_or_create_specification({roll})
    assert len(_find_positionings(rainbow_place, light_saber, roll_specification)) == 0
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, roll_specification) == 0
    assert add_quantity_of_things(rainbow_place, light_saber, roll_specification, 3) == 3
    assert len(_find_positionings(rainbow_place, light_saber, roll_specification)) == 1
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, roll_specification) == 3

    # Force a redundant entry. Should not happen if only using add_quantity_of_things
    # but worth checking that the code is robust enough to deal with it.
    positioning = Positioning(thing=light_saber, specification=roll_specification, place=rainbow_place, quantity=100)
    database.session.add(positioning)
    database.session.commit()
    assert len(_find_positionings(rainbow_place, light_saber, roll_specification)) == 2  # redundant entries
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, roll_specification) == 103

    assert add_quantity_of_things(rainbow_place, light_saber, roll_specification, 4) == 107
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, roll_specification) == 107

    assert len(_find_positionings(rainbow_place, light_saber, roll_specification)) == 1  # back to just one entry


def test_change_of_place(rainbow_place, wild_place, light_saber, knights_of_the_round_table, roll):
    roll_specification = knights_of_the_round_table.find_or_create_specification({roll})
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, roll_specification) == 0
    assert find_exact_quantity_of_things_at_place(wild_place, light_saber, roll_specification) == 0

    assert add_quantity_of_things(rainbow_place, light_saber, roll_specification, 7) == 7
    assert find_exact_quantity_of_things_at_place(rainbow_place, light_saber, roll_specification) == 7
    assert find_exact_quantity_of_things_at_place(wild_place, light_saber, roll_specification) == 0

    assert move_quantity_of_things(Destination(wild_place), rainbow_place, light_saber, roll_specification, 2) == (2, 5)
