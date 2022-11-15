#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.root_forms import RootCreateForm, create_root_from_form
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.viewers.roots_viewer import RootsViewer


class RootsCreateHandler(PageHandler, FormHandler, PlatterHoldingHandler):
    page_template = "pages/form_page.j2"
    objects_are_valid = True
    form_title = "Create New Root"

    def __init__(self, endpoint, viewer):
        PageHandler.__init__(self, endpoint)
        PlatterHoldingHandler.__init__(self, viewer)

    @property
    def cancel_redirect_url(self):
        return self.navigator.target_url(RootsViewer, 'view')

    def create_form(self):
        return RootCreateForm()

    def submit_action(self):
        return create_root_from_form(self.form)

    def success_redirect_url(self, target):
        return self.navigator.target_url(target, 'view')
