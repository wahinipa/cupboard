#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.all_roles import AllRoles
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.page_handlers.view_handler import ViewHandler


class RoleListHandler(PageHandler, ViewHandler, PlatterHoldingHandler):
    page_template = "pages/role_list.j2"

    objects_are_valid = True
    current_activity = "role"

    def __init__(self, endpoint, viewer):
        PageHandler.__init__(self, endpoint)
        PlatterHoldingHandler.__init__(self, viewer)

    @property
    def display_context_maker(self):
        return AllRoles()

    @property
    def display_attributes(self):
        return {
            'add_tasks': True,
            'description': True,
            'url': True,
            'bread_crumbs': True,
            'children_attributes': {
                'role': {
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
