#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.forms.people_forms import UserProfileForm
from tracking.modelling.role_models import Role
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.people_base_handler import PeopleBaseHandler
from tracking.page_handlers.target_update_handler import TargetUpdateHandler


class PeopleUpdateHandler(PeopleBaseHandler, FormHandler, TargetUpdateHandler):
    page_template = 'pages/form_page.j2'
    proper_role_names = [Role.super_role_name, Role.self_role_name]

    def create_form(self):
        return UserProfileForm(obj=self.person)

    def submit_action(self):
        self.form.populate_obj(self.person)
        database.session.commit()
        return self.person
