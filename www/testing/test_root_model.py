#  Copyright (c) 2022, Wahinipa LLC
from testing.fixtures import app, the_root, ROOT_NAME, ROOT_DESCRIPTION, ROOT_PLACE_NAME, ROOT_THING_NAME


def _pycharm_please_keep_these_imports():
    return app, the_root


def test_root_creation(the_root):
    assert the_root is not None
    assert the_root.name == ROOT_NAME
    assert the_root.description == ROOT_DESCRIPTION

    top_place = the_root.place
    assert top_place is not None
    assert top_place.root == the_root
    assert top_place.name == ROOT_PLACE_NAME

    top_thing = the_root.thing
    assert top_thing is not None
    assert top_thing.root == the_root
    assert top_thing.name == ROOT_THING_NAME
