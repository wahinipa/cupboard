#  Copyright (c) 2022, Wahinipa LLC
from tracking.navigation.platter import PlatterById
from tracking.page_handlers.viewer_holding_handler import ViewerHoldingHandler
from tracking.viewers.categories_viewer import CategoriesViewer


class PlatterHoldingHandler(ViewerHoldingHandler):

    def __init__(self, viewer, **kwargs):
        ViewerHoldingHandler.__init__(self, viewer)
        self.platter = PlatterById(**kwargs)

    @property
    def platter_objects_are_valid(self):
        return self.platter.may_be_observed(self.viewer)

    @property
    def navigator(self):
        return self.platter

    @property
    def categories(self):
        return self.platter.categories

    @property
    def category_list_url(self):
        return self.navigator.url(CategoriesViewer, 'view')

    @property
    def current_quantity(self):
        return self.platter.current_quantity

    @property
    def place(self):
        return self.platter.place

    @property
    def place_url(self):
        return self.navigator.url(self.root, 'view')

    @property
    def root(self):
        return self.platter.root

    @property
    def specification(self):
        return self.platter.specification

    @property
    def thing(self):
        return self.platter.thing

    @property
    def thing_specification(self):
        return self.platter.thing_specification
