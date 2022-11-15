#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.people_forms import UserCreateForm, create_user_from_form
from tracking.modelling.people_model import AllPeople
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.people_base_handler import PeopleBaseHandler


class PeopleCreateHandler(PeopleBaseHandler, FormHandler):
    page_template = 'pages/form_page.j2'
    form_title = f'Create New User Account'

    def create_form(self):
        return UserCreateForm()

    @property
    def cancel_redirect_url(self):
        return self.navigator.target_url(AllPeople, 'view', activity=self.activity)

    def submit_action(self):
        return create_user_from_form(self.form)

    def success_redirect_url(self, person):
        return self.navigator.target_url(person, 'view', activity=self.activity)
