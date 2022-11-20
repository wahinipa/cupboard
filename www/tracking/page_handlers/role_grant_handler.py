#  Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking.modelling.role_models import Role, assign_universal_role, assign_root_role, assign_place_role
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler


class RoleGrantHandler(PageHandler, PlatterHoldingHandler):
    def __init__(self, endpoint, viewer, **kwargs):
        PageHandler.__init__(self, endpoint)
        PlatterHoldingHandler.__init__(self, viewer, **kwargs)

    @property
    def objects_are_valid(self):
        return self.person and self.role

    def validated_rendering(self):
        redirect_url = self.navigator.target_url(self.role, 'view', activity=self.activity)
        role_name = self.role and self.role.name
        if self.person:
            if role_name in Role.universal_role_name_set:
                assign_universal_role(self.role, self.person)
            elif self.place:
                if role_name in Role.root_role_name_set:
                    assign_root_role(self.place.root, self.role, self.person)
                elif role_name in Role.place_role_name_set:
                    assign_place_role(self.place, self.role, self.person)
        return redirect(redirect_url)
