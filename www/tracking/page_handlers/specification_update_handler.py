#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.specification_forms import create_specification_form_descriptor, \
    create_dynamic_specification_form, \
    update_specification
from tracking.modelling.category_model import find_category_by_id
from tracking.navigation.platter import Platter
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.target_handler import TargetHandler
from tracking.page_handlers.target_update_handler import TargetUpdateHandler


class SpecificationUpdateHandler(PageHandler, ActivePlatterHoldingHandler, TargetHandler, FormHandler,
                                 TargetUpdateHandler):
    page_template = 'pages/specification_update.j2'

    def __init__(self, endpoint, viewer, category_id=None, **kwargs):
        PageHandler.__init__(self, endpoint)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)
        category = find_category_by_id(category_id)
        self.category = category and category.root == self.root and category
        TargetHandler.__init__(self, self.category and self.specification)
        self.form_descriptor = self.category and self.specification and create_specification_form_descriptor(
            self.category, self.specification)

    @property
    def current_activity(self):
        return self.activity

    def create_form(self):
        return create_dynamic_specification_form(self.form_descriptor)

    def extra_render_template_args(self):
        return {
            'form_descriptor': self.form_descriptor,
        }

    def submit_action(self):
        new_specification = update_specification(self.category, self.specification, self.form)
        self.platter = Platter(viewer=self.viewer, root=self.root, place=self.place, thing=self.thing, destination=self.destination,
                               specification=new_specification, activity=self.activity)
        return self.root

    def target_update_redirect(self):
        return self.navigator.target_url(self.root, 'view', activity=self.activity)
