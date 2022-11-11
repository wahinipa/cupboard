#  Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking import database
from tracking.page_handlers.people_base_handler import PeopleBaseHandler


class PeopleDisableHandler(PeopleBaseHandler):

    def validated_rendering(self):
        redirect_url = self.navigator.url(self.person, 'view', activity=self.activity)
        self.person.is_enabled = False
        database.session.commit()
        return redirect(redirect_url)

    @property
    def viewer_has_permission(self):
        return self.target and self.viewer.may_disable_person(self.person)
