#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.particular_thing_model import find_particular_thing_by_id
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.root_model import find_root_by_id
from tracking.modelling.specification_model import find_specification_by_id
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.dual_navigator import DualNavigator


class Placement:
    def __init__(self, root=None, place=None, thing=None, specification=None, particular_thing=None):
        if root is None:
            if place:
                root = place.root
            elif thing:
                root = thing.root
            elif specification:
                root = specification.root
        if root:
            place = place or root.place
            thing = thing or root.thing
            specification = specification or root.generic_specification
        self.root = root
        self.place = place
        self.thing = thing
        self.specification = specification
        self.particular_thing = particular_thing

    @property
    def is_valid(self):
        return self.root and self.thing and self.place and self.specification \
               and self.thing.root == self.root and self.place.root == self.root \
               and self.specification.root == self.root

    def may_be_observed(self, viewer):
        return self.is_valid and self.root.may_be_observed(viewer)

    def create_navigator(self):
        return DualNavigator(place=self.place, thing=self.thing, particular_thing=self.particular_thing)


def create_placement(root_id=None, place_id=None, thing_id=None, specification_id=None, particular_thing_id=None):
    if root_id:
        root = find_root_by_id(root_id)
    else:
        root = None
    if place_id:
        place = find_place_by_id(place_id)
    else:
        place = None
    if thing_id:
        thing = find_thing_by_id(thing_id)
    else:
        thing = None
    if specification_id:
        specification = find_specification_by_id(specification_id)
    else:
        specification = None
    if particular_thing_id:
        particular_thing = find_particular_thing_by_id(particular_thing_id)
    else:
        particular_thing = None
    if particular_thing:
        thing = thing or particular_thing.thing
        specification = specification or particular_thing.specification
    return Placement(root=root, place=place, thing=thing, specification=specification,
                     particular_thing=particular_thing)
