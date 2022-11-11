#  Copyright (c) 2022, Wahinipa LLC
from tracking.navigation.cupboard_navigation import create_cupboard_navigator
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.page_handlers.viewer_holding_handler import ViewerHoldingHandler
from tracking.viewers.people_list_viewer import PeopleListViewer


class PeopleListHandler(PageHandler, ViewHandler, ViewerHoldingHandler):
    page_template = "pages/people_list.j2"
    viewer_has_permission = True
    objects_are_valid = True
    current_activity = "people"

    def __init__(self, viewer):
        ViewerHoldingHandler.__init__(self, viewer)
        self.navigator = create_cupboard_navigator()
        self.root = None

    @property
    def display_context_maker(self):
        return PeopleListViewer()

    @property
    def display_attributes(self):
        return {
            'description': True,
            'url': True,
            'bread_crumbs': True,
            'children_attributes': {
                'people': {
                    'notation': True,
                },
            },
        }

    @property
    def destination_inventory(self):
        return None

    @property
    def source_inventory(self):
        return None
