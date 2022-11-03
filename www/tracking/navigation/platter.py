#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.place_model import find_place_by_id
from tracking.modelling.positioning_mixin import current_quantity
from tracking.modelling.root_model import find_root_by_id
from tracking.modelling.specification_model import find_specification_by_id
from tracking.modelling.thing_model import find_thing_by_id
from tracking.navigation.navigating_platter import NavigatingPlatter
from tracking.viewers.thing_specification import ThingSpecification


class Platter(NavigatingPlatter):

    @property
    def is_valid(self):
        return self.root and self.thing and self.place and self.specification \
               and self.thing.root == self.root and self.place.root == self.root \
               and self.specification.root == self.root

    def may_be_observed(self, viewer):
        return self.is_valid and self.root.may_be_observed(viewer)

    @property
    def thing_specification(self):
        return ThingSpecification(self.thing, self.specification)

    @property
    def current_quantity(self):
        return current_quantity(self.place, self.thing, self.specification)


class PlatterById(Platter):
    def __init__(self, activity='explore', root_id=None, place_id=None, thing_id=None, specification_id=None):
        root = root_id and find_root_by_id(root_id)
        place = place_id and find_place_by_id(place_id)
        thing = thing_id and find_thing_by_id(thing_id)
        specification = specification_id and find_specification_by_id(specification_id)
        Platter.__init__(self, activity=activity, root=root, place=place, thing=thing, specification=specification)
