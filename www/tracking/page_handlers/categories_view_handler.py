#  Copyright (c) 2022, Wahinipa LLC

from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.modelling.role_models import Role
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.viewers.model_viewer import ModelViewer


class CategoriesViewHandler(PageHandler, ViewHandler, ActivePlatterHoldingHandler):
    required_role_name = Role.admin_role_name
    page_template = "pages/category_list.j2"
    current_activity = 'category'

    def __init__(self, endpoint, viewer, **kwargs):
        PageHandler.__init__(self, endpoint)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)

    @property
    def display_context_maker(self):
        return ModelViewer(self.root)

    @property
    def display_attributes(self):
        return {
            'description': True,
            'children': [self.categories, self.thing, self.thing_specification],
            'children_attributes': dual_view_childrens_attributes(),
        }
