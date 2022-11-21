#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler


class PeopleBaseHandler(PageHandler, PlatterHoldingHandler):
    current_activity = 'people'  # This lights up the 'People' button in the top menu.
    category_list_url = None
    place_url = None

    def __init__(self, endpoint, viewer, person_id=None):
        PageHandler.__init__(self, endpoint)
        PlatterHoldingHandler.__init__(self, viewer, person_id=person_id)
        self.target = self.person
