#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.viewers.roots_viewer import RootsViewer


class RootsViewHandler(PageHandler, ViewHandler, PlatterHoldingHandler):
    page_template = "pages/home_page.j2"
    viewer_has_permission = True
    objects_are_valid = True
    active_flavor = "home"

    def __init__(self, viewer):
        PlatterHoldingHandler.__init__(self, viewer)

    @property
    def display_context_maker(self):
        return RootsViewer()

    @property
    def display_attributes(self):
        return {
            'description': True,
            'url': True,
            'bread_crumbs': True,
            'children_attributes': {
                'root': {
                    'display_context': {
                        'description': True,
                        'url': True,
                    },
                },
            },
        }
