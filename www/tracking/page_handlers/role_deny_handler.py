#  Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking.modelling.role_models import remove_role
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler


class RoleDenyHandler(PageHandler, PlatterHoldingHandler):
    def __init__(self, endpoint, viewer, **kwargs):
        PageHandler.__init__(self, endpoint)
        PlatterHoldingHandler.__init__(self, viewer, **kwargs)

    @property
    def objects_are_valid(self):
        return self.person and self.role

    def validated_rendering(self):
        redirect_url = self.navigator.target_url(self.role, 'view', activity=self.activity)
        if self.person:
            remove_role(self.role, self.person, place=self.place)
        return redirect(redirect_url)
