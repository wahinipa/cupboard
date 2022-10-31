#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.platter import create_platter


class PlatterHoldingHandlerMixin:

    def __init__(self, root_id=None, place_id=None, thing_id=None, specification_id=None):
        self.platter = create_platter(root_id=root_id, place_id=place_id, thing_id=thing_id,
                                          specification_id=specification_id)

    def create_navigator(self):
        return self.platter.create_navigator()

    @property
    def objects_are_valid(self):
        return self.platter.may_be_observed(self.viewer)

