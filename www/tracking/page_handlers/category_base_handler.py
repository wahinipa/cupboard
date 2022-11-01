#  Copyright (c) 2022, Wahinipa LLC

from tracking.modelling.category_model import find_category_by_id
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.page_handlers.target_handler import TargetHandler


class CategoryBaseHandler(PageHandler, PlatterHoldingHandler, TargetHandler):
    active_flavor = 'category'  # This lights up the 'Categories' button in the top menu.

    def __init__(self, viewer, category_id, place_id, thing_id, specification_id):
        PageHandler.__init__(self)
        PlatterHoldingHandler.__init__(self, viewer, place_id=place_id, thing_id=thing_id,
                                       specification_id=specification_id)
        TargetHandler.__init__(self, find_category_by_id(category_id))

    @property
    def category(self):
        return self.target