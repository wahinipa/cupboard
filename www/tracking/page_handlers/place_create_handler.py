#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.place_forms import PlaceCreateForm
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.place_base_handler import PlaceBaseHandler


class PlaceCreateHandler(PlaceBaseHandler, FormHandler):
    page_template = 'pages/form_page.j2'

    @property
    def viewer_has_permission(self):
        return self.place.may_create_place(self.viewer)

    def create_form(self):
        return PlaceCreateForm()

    @property
    def form_title(self):
        return f'Create New Place for {self.place.name}'

    def submit_action(self):
        return self.place.create_kind_of_place(name=self.form.name.data, description=self.form.description.data)

    @property
    def cancel_redirect_url(self):
        return self.navigator.url(self.place, 'view', activity=self.activity)

    def success_redirect_url(self, target):
        return self.navigator.url(target, 'view', activity=self.activity)
