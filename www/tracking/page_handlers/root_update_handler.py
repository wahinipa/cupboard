#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.forms.root_forms import RootUpdateForm, update_root_from_form
from tracking.page_handlers.form_handler import FormHandler
from tracking.page_handlers.root_base_handler import RootBaseHandler
from tracking.page_handlers.target_update_handler import TargetUpdateHandler


class RootUpdateHandler(RootBaseHandler, FormHandler, TargetUpdateHandler):
    page_template = 'pages/form_page.j2'

    def create_form(self):
        return RootUpdateForm(obj=self.root)

    def submit_action(self):
        update_root_from_form(self.root, self.form)
        database.session.commit()
        return self.root
