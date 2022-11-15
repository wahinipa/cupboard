#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler


class InventoryBaseHandler(FormHandler, PageHandler, ActivePlatterHoldingHandler):
    page_template = 'pages/form_page.j2'

    def __init__(self, endpoint, viewer, **kwargs):
        PageHandler.__init__(self, endpoint)
        FormHandler.__init__(self)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)

    @property
    def cancel_redirect_url(self):
        return self.redirect_url

    @property
    def description(self):
        return self.thing_specification.name

    @property
    def redirect_url(self):
        return self.navigator.target_url(self.root, 'view', activity=self.activity)

    def success_redirect_url(self, target):
        return self.redirect_url
