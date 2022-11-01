#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.forms.place_forms import PlaceUpdateForm, update_place_from_form
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.place_base_handler import PlaceBaseHandler
from tracking.page_handlers.target_update_handler import TargetUpdateHandler


class PlaceUpdateHandler(PlaceBaseHandler, FormHandler, TargetUpdateHandler):
    page_template = 'pages/form_page.j2'

    def create_form(self):
        return PlaceUpdateForm(obj=self.place)

    def submit_action(self):
        update_place_from_form(self.place, self.form)
        database.session.commit()
        return self.place
