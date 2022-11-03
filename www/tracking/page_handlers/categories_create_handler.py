#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.category_forms import CategoryCreateForm
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler
from tracking.viewers.categories_model import Categories


class CategoriesCreateHandler(FormHandler, PageHandler, ActivePlatterHoldingHandler):
    page_template = 'pages/form_page.j2'

    def __init__(self, viewer, **kwargs):
        PageHandler.__init__(self)
        FormHandler.__init__(self)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)

    @property
    def cancel_redirect_url(self):
        return self.navigator.url(Categories, 'view')

    @property
    def description(self):
        return self.thing_specification.name

    def success_redirect_url(self, target):
        return self.navigator.url(target, 'view')

    @property
    def viewer_has_permission(self):
        return True

    def create_form(self):
        return CategoryCreateForm()

    @property
    def form_title(self):
        return f'Create New Category for {self.root.name}'

    def submit_action(self):
        return self.root.create_category(self.form.name.data, self.form.description.data)
