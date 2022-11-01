#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.forms.category_forms import update_category_from_form, CategoryUpdateForm
from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.page_handlers.form_handler import FormHandler


class CategoryUpdateHandler(CategoryBaseHandler, FormHandler):
    page_template = 'pages/form_page.j2'

    @property
    def viewer_has_permission(self):
        return self.category.may_update(self.viewer)

    def create_form(self):
        return CategoryUpdateForm(obj=self.category)

    @property
    def form_title(self):
        return f'Update {self.category.name}'

    def submit_action(self):
        category = update_category_from_form(self.category, self.form)
        database.session.commit()
        return category

    @property
    def cancel_redirect_url(self):
        return self.redirect_url

    @property
    def redirect_url(self):
        return self.navigator.url(self.category, 'view')

    def success_redirect_url(self, target):
        return self.redirect_url

