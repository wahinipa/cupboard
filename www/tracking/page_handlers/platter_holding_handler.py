#  Copyright (c) 2022, Wahinipa LLC
from tracking.navigation.platter import PlatterById
from tracking.viewers.categories_viewer import CategoriesViewer


class PlatterHoldingHandler:

    def __init__(self, viewer, **kwargs):
        self.viewer = viewer
        self.platter = PlatterById(viewer=viewer, **kwargs)

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
        return self.navigator.target_url(CategoriesViewer, 'view')

    @property
    def current_quantity(self):
        return self.platter.current_quantity

    @property
    def destination(self):
        return self.platter.destination

    @property
    def person(self):
        return self.platter.person

    @property
    def place(self):
        return self.platter.place

    @property
    def source_inventory(self):
        return self.platter.source_inventory

    @property
    def destination_inventory(self):
        return self.platter.destination_inventory

    @property
    def observe_url(self):
        return self.navigator.target_url(self.root, 'view', activity='observe')

    @property
    def inbound_url(self):
        return self.navigator.target_url(self.root, 'view', activity='inbound')

    @property
    def outbound_url(self):
        return self.navigator.target_url(self.root, 'view', activity='outbound')

    @property
    def transfer_url(self):
        return self.navigator.target_url(self.root, 'view', activity='transfer')

    @property
    def adjust_url(self):
        return self.navigator.target_url(self.root, 'view', activity='adjust')

    @property
    def place_url(self):
        return self.navigator.target_url(self.root, 'view')

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

    @property
    def activity(self):
        return self.platter.activity
