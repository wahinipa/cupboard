#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandlerMixin


class InventoryBaseHandler(FormHandler, PageHandler, PlatterHoldingHandlerMixin):
    page_template = 'pages/form_page.j2'

    def __init__(self, viewer, place_id, thing_id, specification_id):
        PageHandler.__init__(self)
        FormHandler.__init__(self)
        PlatterHoldingHandlerMixin.__init__(self, viewer, place_id=place_id, thing_id=thing_id,
                                              specification_id=specification_id)

    @property
    def cancel_redirect_url(self):
        return self.redirect_url

    @property
    def description(self):
        return self.thing_specification.name

    @property
    def redirect_url(self):
        return self.navigator.url(self.root, 'view')

    def success_redirect_url(self, target):
        return self.redirect_url

    @property
    def viewer_has_permission(self):
        return self.may_be_observed
