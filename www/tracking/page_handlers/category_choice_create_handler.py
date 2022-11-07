#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.choice_forms import ChoiceCreateForm
from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.page_handlers.form_handler import FormHandler


class CategoryChoiceCreateHandler(CategoryBaseHandler, FormHandler):
    page_template = 'pages/form_page.j2'

    @property
    def viewer_has_permission(self):
        return self.category.may_create_choice(self.viewer)

    def create_form(self):
        return ChoiceCreateForm()

    @property
    def form_title(self):
        return f'Create New Choice for {self.category.name}'

    def submit_action(self):
        return self.category.create_choice(self.form.name.data, self.form.description.data)

    @property
    def cancel_redirect_url(self):
        return self.navigator.url(self.category, 'view', activity=self.activity)

    def success_redirect_url(self, target):
        return self.navigator.url(target, 'view', activity=self.activity)
