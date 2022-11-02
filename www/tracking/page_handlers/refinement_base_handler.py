#  Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking.modelling.category_model import find_category_by_id
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler


class RefinementBaseHandler(PageHandler, PlatterHoldingHandler):

    def __init__(self, viewer, category_id, place_id, thing_id, specification_id):
        PageHandler.__init__(self)
        PlatterHoldingHandler.__init__(self, viewer, place_id=place_id, thing_id=thing_id,
                                       specification_id=specification_id)
        category = find_category_by_id(category_id)
        self.category = category and category.root == self.root and category

    @property
    def objects_are_valid(self):
        return self.category

    @property
    def viewer_has_permission(self):
        return self.category.may_update(self.viewer)

    def validated_rendering(self):
        navigator = self.create_navigator()
        redirect_url = navigator.url(self.category, 'view')
        self.change_refinement()
        return redirect(redirect_url)
