#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.root_view_handler import RootViewHandler
from tracking.viewers.inventory_viewer import InventoryViewer


class RootObserveHandler(RootViewHandler):
    page_template = 'pages/root_view.j2'

    @property
    def children(self):
        return [self.place, self.thing, self.thing_specification, InventoryViewer(self.platter)]

