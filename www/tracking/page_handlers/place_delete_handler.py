#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.place_base_handler import PlaceBaseHandler
from tracking.page_handlers.target_delete_handler import TargetDeleteHandler


class PlaceDeleteHandler(PlaceBaseHandler, TargetDeleteHandler):

    @property
    def delete_redirect_url(self):
        return self.navigator.url(self.place.parent_object, 'view')
