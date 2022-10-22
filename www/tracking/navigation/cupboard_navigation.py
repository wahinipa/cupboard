#  Copyright (c) 2022, Wahinipa LLC
from tracking.navigation.categories_navigation import register_categories_navigation
from tracking.navigation.category_navigation import register_category_navigation
from tracking.navigation.choice_navigation import register_choice_navigation
from tracking.navigation.navigator import Navigator
from tracking.navigation.people_navigation import register_people_navigation
from tracking.navigation.place_navigation import register_place_navigation
from tracking.navigation.refinement_navigation import register_refinement_navigation
from tracking.navigation.roots_navigation import register_roots_navigation
from tracking.navigation.root_navigation import register_root_navigation
from tracking.navigation.thing_navigation import register_thing_navigation


def create_cupboard_navigator():
    navigator = Navigator()
    register_categories_navigation(navigator)
    register_category_navigation(navigator)
    register_choice_navigation(navigator)
    register_people_navigation(navigator)
    register_place_navigation(navigator)
    register_refinement_navigation(navigator)
    register_root_navigation(navigator)
    register_roots_navigation(navigator)
    register_thing_navigation(navigator)
    return navigator