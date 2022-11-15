from tracking.page_handlers.active_platter_holding_handler import ActivePlatterHoldingHandler
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.target_handler import TargetHandler


class RootBaseHandler(PageHandler, ActivePlatterHoldingHandler, TargetHandler):

    def __init__(self, endpoint, viewer, **kwargs):
        PageHandler.__init__(self, endpoint)
        ActivePlatterHoldingHandler.__init__(self, viewer, **kwargs)
        TargetHandler.__init__(self, self.root)  # Depends on ActivePlatterHoldingHandler to have created self.root

    @property
    def current_activity(self):
        return self.activity

