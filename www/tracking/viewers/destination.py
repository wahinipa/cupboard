#  Copyright (c) 2022, Wahinipa LLC
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.cardistry_models import bread_crumbs


class Destination(CupboardDisplayContextMixin):
    flavor = "destination"
    singular_label = "Place"
    plural_label = "Destinations"
    possible_tasks = []
    label_prefixes = {}

    def __init__(self, place_model):
        self.place_model = place_model

    def add_description(self, context):
        return self.place_model.add_description(context)

    def bread_crumbs(self, navigator):
        path = self.root_path
        return bread_crumbs(navigator, path, target=path[-1])

    @property
    def id(self):
        return self.place_model.id

    @property
    def label(self):
        return self.place_model.label

    @property
    def name(self):
        return self.place_model.name

    @property
    def root(self):
        return self.place_model.root

    @property
    def root_path(self):
        return [Destination(destination) for destination in self.place_model.root_path]

    def viewable_children(self, viewer):
        return [Destination(destination) for destination in self.place_model.sorted_children]

    @property
    def full_set(self):
        return self.place_model.full_set

    @property
    def full_positionings(self):
        return self.place_model.full_positionings

    @property
    def positionings(self):
        return self.place_model.positionings
