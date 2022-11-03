#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler


class ActivePlatterHoldingHandler(PlatterHoldingHandler):

    @property
    def is_valid(self):
        return self.platter.is_valid

    @property
    def may_be_observed(self):
        return self.platter.may_be_observed(self.viewer)

    # This method allows derived classes to override @property objects_are_valid
    # and still call this parent method without confusing syntax.
    def base_says_objects_are_valid(self):
        return self.platter_objects_are_valid

    @property
    def objects_are_valid(self):
        return self.base_says_objects_are_valid()

