#  Copyright (c) 2022, Wahinipa LLC

from tracking.modelling.category_model import find_category_by_id
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandlerMixin


class CategoryBaseHandler(PageHandler, PlatterHoldingHandlerMixin):
    def __init__(self, viewer, category_id, place_id, thing_id, specification_id):
        PageHandler.__init__(self)
        PlatterHoldingHandlerMixin.__init__(self, viewer, place_id=place_id, thing_id=thing_id,
                                            specification_id=specification_id)
        self.category = find_category_by_id(category_id)

    @property
    def objects_are_valid(self):
        return self.category and self.base_says_objects_are_valid()
