#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.people_model import find_user_by_id
from tracking.navigation.navigating_platter import NavigatingPlatter
from tracking.page_handlers.page_handler import PageHandler
from tracking.page_handlers.viewer_holding_handler import ViewerHoldingHandler


class PeopleBaseHandler(PageHandler, ViewerHoldingHandler):
    active_flavor = 'people'  # This lights up the 'People' button in the top menu.
    category_list_url = None
    place_url = None

    def __init__(self, viewer, user_id=None):
        PageHandler.__init__(self)
        ViewerHoldingHandler.__init__(self, viewer)
        if user_id:
            self.person = find_user_by_id(user_id)
            self.objects_are_valid = self.person is not None
        else:
            self.person = None
            self.objects_are_valid = True
        self.target = self.person
        self.navigator = NavigatingPlatter()
