#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.category_forms import CategoryCreateForm
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler
from tracking.viewers.categories_viewer import CategoriesViewer


class CategoriesCreateHandler(FormHandler, PageHandler, ActivePlatterHoldingHandler):
    page_template = 'pages/form_page.j2'

    def __init__(self, endpoint, viewer, **kwargs):
        PageHandler.__init__(self, endpoint)
        FormHandler.__init__(self)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)

    @property
    def cancel_redirect_url(self):
        return self.navigator.target_url(CategoriesViewer, 'view', activity=self.activity)

    @property
    def description(self):
        return self.thing_specification.name

    def success_redirect_url(self, target):
        return self.navigator.target_url(target, 'view', activity=self.activity)

    def create_form(self):
        return CategoryCreateForm()

    @property
    def form_title(self):
        return f'Create New Category for {self.root.name}'

    def submit_action(self):
        return self.root.create_category(self.form.name.data, self.form.description.data)
