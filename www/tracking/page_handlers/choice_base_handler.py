#  Copyright (c) 2022, Wahinipa LLC

from tracking.modelling.choice_model import find_choice_by_id
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.page_handlers.target_handler import TargetHandler


class ChoiceBaseHandler(PageHandler, PlatterHoldingHandler, TargetHandler):
    active_flavor = 'category'  # This lights up the 'Categories' button in the top menu. There is no 'Choices' button

    def __init__(self, viewer, choice_id=None, **kwargs):
        PageHandler.__init__(self)
        PlatterHoldingHandler.__init__(self, viewer, **kwargs)
        TargetHandler.__init__(self, find_choice_by_id(choice_id))

    @property
    def choice(self):
        return self.target
