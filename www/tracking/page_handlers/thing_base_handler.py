#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler
from tracking.page_handlers.target_handler import TargetHandler


class ThingBaseHandler(PageHandler, ActivePlatterHoldingHandler, TargetHandler):
    current_activity = 'place'  # This lights up the 'Place' button in the top menu.

    def __init__(self, viewer, **kwargs):
        PageHandler.__init__(self)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)
        TargetHandler.__init__(self, self.thing)  # Depends on ActivePlatterHoldingHandler to have created self.thing
