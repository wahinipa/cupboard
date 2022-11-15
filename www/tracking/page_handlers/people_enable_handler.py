#  Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking import database
from tracking.modelling.role_models import Role
from tracking.page_handlers.people_base_handler import PeopleBaseHandler


class PeopleEnableHandler(PeopleBaseHandler):
    proper_role_names = [Role.super_role_name]

    def validated_rendering(self):
        redirect_url = self.navigator.url(self.person, 'view', activity=self.activity)
        self.person.is_enabled = True
        database.session.commit()
        return redirect(redirect_url)

