#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.people_model import AllPeople
from tracking.modelling.role_models import Role
from tracking.page_handlers.people_base_handler import PeopleBaseHandler
from tracking.page_handlers.target_delete_handler import TargetDeleteHandler


class PeopleDeleteHandler(PeopleBaseHandler, TargetDeleteHandler):
    proper_role_names = [Role.super_role_name]

    @property
    def delete_redirect_url(self):
        return self.navigator.target_url(AllPeople, 'view')
