#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.placement_model import create_placement


class PlacementHoldingHandlerMixin:

    def __init__(self, root_id=None, place_id=None, thing_id=None, specification_id=None):
        self.placement = create_placement(root_id=root_id, place_id=place_id, thing_id=thing_id,
                                          specification_id=specification_id)

    def create_navigator(self):
        return self.placement.create_navigator()

    @property
    def objects_are_valid(self):
        return self.placement.may_be_observed(self.viewer)

