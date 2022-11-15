#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.viewers.roots_viewer import RootsViewer


class RootsViewHandler(PageHandler, ViewHandler, PlatterHoldingHandler):
    page_template = "pages/home_page.j2"
    objects_are_valid = True
    current_activity = "home"

    def __init__(self, endpoint, viewer):
        PageHandler.__init__(self, endpoint)
        PlatterHoldingHandler.__init__(self, viewer)

    @property
    def display_context_maker(self):
        return RootsViewer()

    @property
    def display_attributes(self):
        return {
            'add_tasks': True,
            'description': True,
            'url': True,
            'bread_crumbs': True,
            'children_attributes': {
                'root': {
                    'display_context': {
                        'add_tasks': True,
                        'description': True,
                        'url': True,
                    },
                },
            },
        }
