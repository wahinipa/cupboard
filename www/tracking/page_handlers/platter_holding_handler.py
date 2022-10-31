#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.platter import create_platter


class PlatterHoldingHandlerMixin:

    def __init__(self, viewer, root_id=None, place_id=None, thing_id=None, specification_id=None):
        self.viewer = viewer
        self.platter = create_platter(root_id=root_id, place_id=place_id, thing_id=thing_id,
                                          specification_id=specification_id)

    def create_navigator(self):
        return self.platter.create_navigator()

    @property
    def current_quantity(self):
        return self.platter.current_quantity

    @property
    def is_valid(self):
        return self.platter.is_valid

    @property
    def may_be_observed(self):
        return self.platter.may_be_observed(self.viewer)

    @property
    def objects_are_valid(self):
        return self.platter.may_be_observed(self.viewer)

    @property
    def place(self):
        return self.platter.place

    @property
    def root(self):
        return self.platter.root

    @property
    def specification(self):
        return self.platter.specification

    @property
    def thing(self):
        return self.platter.thing

    @property
    def thing_specification(self):
        return self.platter.thing_specification

