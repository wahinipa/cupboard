#  Copyright (c) 2022, Wahinipa LLC
from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.page_handlers.root_base_handler import RootBaseHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.viewers.inventory_viewer import InventoryViewer
from tracking.viewers.model_viewer import ModelViewer


class RootViewHandler(RootBaseHandler, ViewHandler):
    page_template = 'pages/root_view.j2'

    @property
    def display_context_maker(self):
        return ModelViewer(self.root)

    @property
    def display_attributes(self):
        return {
            'children': [self.place, self.thing, self.thing_specification, InventoryViewer(self.platter)],
            'children_attributes': dual_view_childrens_attributes(thing=self.thing),
        }
