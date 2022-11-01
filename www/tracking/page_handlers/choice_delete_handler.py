#  Copyright (c) 2022, Wahinipa LLC

from tracking.page_handlers.choice_base_handler import ChoiceBaseHandler
from tracking.page_handlers.target_delete_handler import TargetDeleteHandler


class ChoiceDeleteHandler(ChoiceBaseHandler, TargetDeleteHandler):

    @property
    def delete_redirect_url(self):
        return self.navigator.url(self.choice.category, 'view')
