#  Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking.modelling.category_model import find_category_by_id
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler


class RefinementBaseHandler(PageHandler, ActivePlatterHoldingHandler):

    def __init__(self, endpoint, viewer, category_id=None, **kwargs):
        PageHandler.__init__(self, endpoint)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)
        category = find_category_by_id(category_id)
        self.category = category and category.root == self.root and category

    @property
    def objects_are_valid(self):
        return self.category

    def validated_rendering(self):
        redirect_url = self.navigator.target_url(self.category, 'view')
        self.change_refinement()
        return redirect(redirect_url)
