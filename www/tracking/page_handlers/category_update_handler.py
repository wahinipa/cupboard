#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.forms.category_forms import update_category_from_form, CategoryUpdateForm
from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.target_update_handler import TargetUpdateHandler


class CategoryUpdateHandler(CategoryBaseHandler, FormHandler, TargetUpdateHandler):
    page_template = 'pages/form_page.j2'

    def create_form(self):
        return CategoryUpdateForm(obj=self.category)

    def submit_action(self):
        category = update_category_from_form(self.category, self.form)
        database.session.commit()
        return category
