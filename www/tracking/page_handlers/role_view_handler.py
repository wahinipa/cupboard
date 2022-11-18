#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.viewers.all_roles import AllRoles
from tracking.viewers.role_viewer import RoleViewer


class RoleViewHandler(PageHandler, PlatterHoldingHandler, ViewHandler):
    current_activity = 'role'

    def __init__(self, endpoint, viewer, role_id=None, place_id=None, person_id=None):
        PageHandler.__init__(self, endpoint)
        PlatterHoldingHandler.__init__(self, viewer, place_id=place_id, user_id=person_id, activity='role',
                                       role_id=role_id)
        if self.role:
            self.page_viewer = RoleViewer(place=self.place, person=self.person, role=self.role)
        else:
            self.page_viewer = AllRoles(place=self.place, person=self.person)

    @property
    def display_context_maker(self):
        return self.page_viewer

    @property
    def page_template(self):
        return self.page_viewer.page_template

    @property
    def objects_are_valid(self):
        return True

    @property
    def display_attributes(self):
        return self.page_viewer.display_attributes
