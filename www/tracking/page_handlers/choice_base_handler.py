#  Copyright (c) 2022, Wahinipa LLC

from tracking.modelling.choice_model import find_choice_by_id
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler
from tracking.page_handlers.target_handler import TargetHandler


class ChoiceBaseHandler(PageHandler, ActivePlatterHoldingHandler, TargetHandler):
    current_activity = 'category'  # This lights up the 'Categories' button in the top menu. There is no 'Choices' button

    def __init__(self, endpoint, viewer, choice_id=None, **kwargs):
        PageHandler.__init__(self, endpoint)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)
        TargetHandler.__init__(self, find_choice_by_id(choice_id))

    @property
    def choice(self):
        return self.target
