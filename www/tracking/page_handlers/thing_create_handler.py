#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.thing_forms import ThingCreateForm
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.thing_base_handler import ThingBaseHandler


class ThingCreateHandler(ThingBaseHandler, FormHandler):
    page_template = 'pages/form_page.j2'

    def create_form(self):
        return ThingCreateForm()

    @property
    def form_title(self):
        return f'Create New Kind of {self.thing.name}'

    def submit_action(self):
        return self.thing.create_kind_of_thing(name=self.form.name.data, description=self.form.description.data)

    @property
    def cancel_redirect_url(self):
        return self.navigator.target_url(self.thing, 'view', activity=self.activity)

    def success_redirect_url(self, target):
        return self.navigator.target_url(target, 'view')
