#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.forms.thing_forms import ThingUpdateForm, update_thing_from_form
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.target_update_handler import TargetUpdateHandler
from tracking.page_handlers.thing_base_handler import ThingBaseHandler


class ThingUpdateHandler(ThingBaseHandler, FormHandler, TargetUpdateHandler):
    page_template = 'pages/form_page.j2'

    def create_form(self):
        return ThingUpdateForm(obj=self.thing)

    def submit_action(self):
        update_thing_from_form(self.thing, self.form)
        database.session.commit()
        return self.place
