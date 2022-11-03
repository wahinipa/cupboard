#  Copyright (c) 2022, Wahinipa LLC
from tracking.navigation.navigating_platter import NavigatingPlatter
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.viewers.roots_viewer import RootsViewer


class RootsViewHandler(PageHandler, PlatterHoldingHandler):
    viewer_has_permission = True
    objects_are_valid = True

    def __init__(self, viewer):
        PlatterHoldingHandler.__init__(self, viewer)

    def validated_rendering(self):
        navigator = NavigatingPlatter()
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
        return roots.display_context(self.navigator, self.viewer, display_attributes).render_template(
            "pages/home_page.j2", active_flavor="home")
