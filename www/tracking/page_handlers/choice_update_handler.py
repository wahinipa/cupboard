#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.forms.choice_forms import ChoiceUpdateForm, update_choice_from_form
from tracking.modelling.role_models import Role
from tracking.page_handlers.choice_base_handler import ChoiceBaseHandler
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.target_update_handler import TargetUpdateHandler


class ChoiceUpdateHandler(ChoiceBaseHandler, FormHandler, TargetUpdateHandler):
    required_role_name = Role.admin_role_name
    page_template = 'pages/form_page.j2'

    def create_form(self):
        return ChoiceUpdateForm(obj=self.choice)

    def submit_action(self):
        choice = update_choice_from_form(self.choice, self.form)
        database.session.commit()
        return choice
