#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.people_model import AllPeople
from tracking.page_handlers.people_base_handler import PeopleBaseHandler
from tracking.page_handlers.target_delete_handler import TargetDeleteHandler


class PeopleDeleteHandler(PeopleBaseHandler, TargetDeleteHandler):

    @property
    def delete_redirect_url(self):
        return self.navigator.url(AllPeople, 'view')

    @property
    def viewer_has_permission(self):
        return self.target and self.viewer.may_delete_person(self.person)
