#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role, find_role_by_id
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.viewers.model_viewer import ModelViewer


class RoleViewHandler(PageHandler, PlatterHoldingHandler, ViewHandler):
    page_template = 'pages/role_view.j2'
    current_activity = 'role'

    def __init__(self, endpoint, viewer, role_id=None):
        PageHandler.__init__(self, endpoint)
        PlatterHoldingHandler.__init__(self, viewer)
        self.role = find_role_by_id(role_id)

    @property
    def display_context_maker(self):
        return ModelViewer(self.role)

    @property
    def objects_are_valid(self):
        return True

    @property
    def display_attributes(self):
        return {
            'add_tasks': True,
            'description': True,
            'url': True,
            'bread_crumbs': True,
        }
