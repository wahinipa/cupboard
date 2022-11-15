#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role
from tracking.page_handlers.place_base_handler import PlaceBaseHandler
from tracking.page_handlers.target_delete_handler import TargetDeleteHandler


class PlaceDeleteHandler(PlaceBaseHandler, TargetDeleteHandler):
    required_role_name= Role.location_manager_name

    @property
    def delete_redirect_url(self):
        return self.navigator.target_url(self.place.parent_object, 'view')
