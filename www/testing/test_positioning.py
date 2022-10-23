#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, rainbow_place, wild_place, light_saber, muffin, roll, pastry, the_root
from tracking import database
from tracking.modelling.particular_thing_model import find_or_create_particular_thing
from tracking.modelling.postioning_model import find_quantity_of_things, add_quantity_of_things, _find_positionings, \
    Positioning, move_quantity_of_things


def _pycharm_please_keep_these_imports():
    return app, rainbow_place, wild_place, light_saber, muffin, roll, pastry, the_root


def test_quantities(rainbow_place, light_saber, the_root, muffin):
    particular_light_saber = find_or_create_particular_thing(light_saber, [muffin])
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 0
    assert add_quantity_of_things(rainbow_place, particular_light_saber, 3) == 3
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 3
    assert add_quantity_of_things(rainbow_place, particular_light_saber, 4) == 7
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 7
    assert add_quantity_of_things(rainbow_place, particular_light_saber, -2) == 5
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 5
    assert rainbow_place.quantity_of_things(particular_light_saber) == 5
    assert particular_light_saber.quantity_at_place(rainbow_place) == 5
    assert rainbow_place.add_to_thing(particular_light_saber, 10) == 15
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 15
    assert particular_light_saber.add_to_place(rainbow_place, 9) == 24
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 24
    assert particular_light_saber.quantity_at_place(rainbow_place) == 24
    assert light_saber.quantity_at_place(rainbow_place) == 24
    everything = light_saber.kind_of
    assert everything is not None
    assert everything.quantity_at_place(rainbow_place) == 24


def test_handles_redundant_quantities(rainbow_place, light_saber, roll, the_root):
    particular_light_saber = find_or_create_particular_thing(light_saber, [roll])
    assert len(_find_positionings(rainbow_place, particular_light_saber)) == 0
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 0
    assert add_quantity_of_things(rainbow_place, particular_light_saber, 3) == 3
    assert len(_find_positionings(rainbow_place, particular_light_saber)) == 1
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 3

    # Force a redundant entry. Should not happen if only using add_quantity_of_things
    # but worth checking that the code is robust enough to deal with it.
    positioning = Positioning(particular_thing=particular_light_saber, place=rainbow_place, quantity=100)
    database.session.add(positioning)
    database.session.commit()
    assert len(_find_positionings(rainbow_place, particular_light_saber)) == 2  # redundant entries
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 103

    assert add_quantity_of_things(rainbow_place, particular_light_saber, 4) == 107
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 107

    assert len(_find_positionings(rainbow_place, particular_light_saber)) == 1  # back to just one entry


def test_change_of_place(rainbow_place, wild_place, light_saber, the_root, roll):
    particular_light_saber = find_or_create_particular_thing(light_saber, [roll])
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 0
    assert find_quantity_of_things(wild_place, particular_light_saber) == 0
    assert add_quantity_of_things(rainbow_place, particular_light_saber, 7) == 7
    assert find_quantity_of_things(rainbow_place, particular_light_saber) == 7
    assert find_quantity_of_things(wild_place, particular_light_saber) == 0
    assert move_quantity_of_things(wild_place, rainbow_place, particular_light_saber, 2) == (2, 5)
