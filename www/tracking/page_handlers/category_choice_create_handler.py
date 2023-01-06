#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.choice_forms import ChoiceCreateForm
from tracking.modelling.role_models import Role
from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.page_handlers.form_handler import FormHandler


class CategoryChoiceCreateHandler(CategoryBaseHandler, FormHandler):
    required_role_name = Role.admin_role_name
    page_template = 'pages/form_page.j2'

    def create_form(self):
        return ChoiceCreateForm()

    @property
    def form_title(self):
        return f'Create New Choice for {self.category.name}'

    def submit_action(self):
        return self.category.create_choice(self.form.name.data, self.form.description.data)

    @property
    def cancel_redirect_url(self):
        return self.navigator.target_url(self.category, 'view', activity=self.activity)

    def success_redirect_url(self, target):
        # Usually the success redirect would be to view the object just created.
        # However, the user is most often creating multiple choices for a category.
        # By returning user instead to the category view the user is saved a step.
        return self.navigator.target_url(self.category, 'view', activity=self.activity)
