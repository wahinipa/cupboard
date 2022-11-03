#  Copyright (c) 2022, Wahinipa LLC

from tracking.modelling.category_model import find_category_by_id
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler
from tracking.page_handlers.target_handler import TargetHandler


class CategoryBaseHandler(PageHandler, ActivePlatterHoldingHandler, TargetHandler):
    active_flavor = 'category'  # This lights up the 'Categories' button in the top menu.

    def __init__(self, viewer, category_id=None, **kwargs):
        PageHandler.__init__(self)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)
        category = find_category_by_id(category_id)
        target = category and category.root == self.root and category
        TargetHandler.__init__(self, target)

    @property
    def category(self):
        return self.target
