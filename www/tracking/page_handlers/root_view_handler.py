#  Copyright (c) 2022, Wahinipa LLC
from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.page_handlers.root_base_handler import RootBaseHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.viewers.model_viewer import ModelViewer


class RootViewHandler(RootBaseHandler, ViewHandler):
    @property
    def display_context_maker(self):
        return ModelViewer(self.root)

    @property
    def display_attributes(self):
        return {
            'children': self.children,
            'children_attributes': dual_view_childrens_attributes(
                thing=self.thing,
                place_prefix=self.place_prefix,
                destination_prefix=self.destination_prefix
            ),
        }
