#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.target_delete_handler import TargetDeleteHandler
from tracking.page_handlers.thing_base_handler import ThingBaseHandler


class ThingDeleteHandler(ThingBaseHandler, TargetDeleteHandler):

    @property
    def delete_redirect_url(self):
        return self.navigator.target_url(self.thing.parent_object, 'view')
