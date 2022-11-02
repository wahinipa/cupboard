#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.specification_forms import create_specification_form_descriptor, \
    create_dynamic_specification_form, \
    update_specification
from tracking.modelling.category_model import find_category_by_id
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.page_handlers.target_handler import TargetHandler
from tracking.page_handlers.target_update_handler import TargetUpdateHandler
from tracking.viewers.platter import Platter


class SpecificationUpdateHandler(PageHandler, PlatterHoldingHandler, TargetHandler, FormHandler, TargetUpdateHandler):
    active_flavor = 'place'  # This lights up the 'Place' button in the top menu.
    page_template = 'pages/form_page.j2'

    def __init__(self, viewer, category_id, place_id, thing_id, specification_id):
        PageHandler.__init__(self)
        PlatterHoldingHandler.__init__(self, viewer, place_id=place_id, thing_id=thing_id,
                                       specification_id=specification_id)
        category = find_category_by_id(category_id)
        self.category = category and category.root == self.root and category
        TargetHandler.__init__(self, self.category and self.specification)
        self.form_descriptor = self.category and self.specification and create_specification_form_descriptor(
            self.category, self.specification)

    def create_form(self):
        return create_dynamic_specification_form(self.form_descriptor)

    def submit_action(self):
        new_specification = update_specification(self.category, self.specification, self.form)
        self.platter = Platter(root=self.root, place=self.place, thing=self.thing,
                               specification=new_specification)
        self.navigator = self.create_navigator()
        return self.root

    def target_update_redirect(self):
        return self.navigator.url(self.root, 'view')
