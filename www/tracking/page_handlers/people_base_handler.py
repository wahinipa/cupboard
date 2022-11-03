#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.people_model import find_user_by_id
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.platter_holding_handler import PlatterHoldingHandler


class PeopleBaseHandler(PageHandler, PlatterHoldingHandler):
    active_flavor = 'people'  # This lights up the 'People' button in the top menu.
    category_list_url = None
    place_url = None

    def __init__(self, viewer, user_id=None):
        PageHandler.__init__(self)
        PlatterHoldingHandler.__init__(self, viewer)
        if user_id:
            self.person = find_user_by_id(user_id)
            self.objects_are_valid = self.person is not None
        else:
            self.person = None
            self.objects_are_valid = True
        self.target = self.person
