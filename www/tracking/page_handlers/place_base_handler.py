#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler
from tracking.page_handlers.target_handler import TargetHandler


class PlaceBaseHandler(PageHandler, PlatterHoldingHandler, TargetHandler):
    active_flavor = 'place'  # This lights up the 'Place' button in the top menu.

    def __init__(self, viewer, place_id, thing_id, specification_id):
        PageHandler.__init__(self)
        PlatterHoldingHandler.__init__(self, viewer, place_id=place_id, thing_id=thing_id,
                                       specification_id=specification_id)
        TargetHandler.__init__(self, self.place)  # Depends on PlatterHoldingHandler to have created self.place
