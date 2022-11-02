#  Copyright (c) 2022, Wahinipa LLC
from tracking.navigation.dual_navigator import DualNavigator
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.viewer_holding_handler import ViewerHoldingHandler
from tracking.viewers.roots_viewer import RootsViewer


class RootsViewHandler(PageHandler, ViewerHoldingHandler):
    viewer_has_permission = True
    objects_are_valid = True

    def __init__(self, viewer):
        ViewerHoldingHandler.__init__(self, viewer)

    def validated_rendering(self):
        navigator = DualNavigator()
        roots = RootsViewer()
        display_attributes = {
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
        return roots.display_context(navigator, self.viewer, display_attributes).render_template("pages/home_page.j2",
                                                                                                 active_flavor="home")
