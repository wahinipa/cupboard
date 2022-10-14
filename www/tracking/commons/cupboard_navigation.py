#  Copyright (c) 2022, Wahinipa LLC
from tracking.navigation.navigator import Navigator
from tracking.navigation.place_navigator import register_place_navigation
from tracking.navigation.root_navigator import register_root_navigation
from tracking.navigation.thing_navigator import register_thing_navigation


def create_cupboard_navigator():
    navigator = Navigator()
    register_root_navigation(navigator)
    register_place_navigation(navigator)
    register_thing_navigation(navigator)
    return navigator
