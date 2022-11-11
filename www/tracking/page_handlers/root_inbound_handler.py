#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.root_view_handler import RootViewHandler
from tracking.viewers.inventory_viewer import InventoryViewer


class RootInboundHandler(RootViewHandler):
    page_template = 'pages/root_view.j2'
    place_prefix = 'Arriving at: '
    destination_prefix = None

    @property
    def children(self):
        return [self.place, self.thing, self.thing_specification]

