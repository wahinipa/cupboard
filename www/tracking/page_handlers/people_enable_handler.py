#  Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking import database
from tracking.page_handlers.people_base_handler import PeopleBaseHandler


class PeopleEnableHandler(PeopleBaseHandler):

    def validated_rendering(self):
        redirect_url = self.navigator.target_url(self.person, 'view', activity=self.activity)
        self.person.is_enabled = True
        database.session.commit()
        return redirect(redirect_url)
