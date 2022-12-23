# Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.viewers.all_roles import AllRoles


class LinkageHandler(PageHandler, PlatterHoldingHandler):
    def __init__(self, endpoint, viewer, **kwargs):
        PageHandler.__init__(self, endpoint)
        PlatterHoldingHandler.__init__(self, viewer, **kwargs)

    @property
    def objects_are_valid(self):
        return self.person and self.place and self.place.root

    def validated_rendering(self):
        redirect_url = self.navigator.target_url(AllRoles, 'view', activity=self.activity)
        root = self.place and self.place.root
        if self.person and root:
            self.action(root)
        return redirect(redirect_url)
