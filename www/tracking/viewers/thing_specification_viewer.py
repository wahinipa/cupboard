#  Copyright (c) 2022, Wahinipa LLC
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.cardistry_models import sorted_by_name
from tracking.modelling.specification_model import describe_choices
from tracking.viewers.Inventory_holder import InventoryHolder
from tracking.viewers.category_specification_viewer import CategorySpecificationViewer


class ThingSpecificationViewer(CupboardDisplayContextMixin, InventoryHolder):
    flavor = 'specification'
    label = 'Specification'
    label_prefixes = {}
    singular_label = 'Specification'
    might_be_possible_tasks = ['arriving', 'moving', 'changing', 'departing']

    def __init__(self, place, destination, thing, specification, activity):
        InventoryHolder.__init__(self, place, thing, specification)
        self.activity = activity
        self.destination = destination
        self.thing_categories = thing.complete_set_of_categories
        self.choices = {choice for choice in specification.choices if choice.category in self.thing_categories}
        self.unknowns = {unknown for unknown in specification.unknowns if unknown in self.thing_categories}

    @property
    def possible_tasks(self):
        return [task for task in self.might_be_possible_tasks if self.task_is_appropriate(task)]

    @property
    def identities(self):
        return {
            'place_id': self.place.id,
            'thing_id': self.thing.id,
            'destination_id': self.destination.id,
            'specification_id': self.specification.id
        }

    def add_description(self, context):
        pass

    def choices_for(self, category):
        return {choice for choice in self.choices if choice.category == category}

    @property
    def is_specific(self):
        found_categories = set(self.unknowns)
        for choice in self.choices:
            category = choice.category
            if category in found_categories:
                return False  # multiple choices for this category
            found_categories.add(category)
        return found_categories == self.thing_categories

    @property
    def name(self):
        description = describe_choices(self.choices, self.unknowns)
        return f'{description} --- {self.thing.name}'

    def viewable_children(self, viewer):
        sorted_categories = sorted_by_name(list(self.thing.complete_set_of_categories))
        return [CategorySpecificationViewer(category, self) for category in sorted_categories]

    def task_is_appropriate(self, task):
        if self.is_specific:
            have_some = self.quantity > 0
            if task == 'arriving':
                return self.activity == 'inbound'
            elif task == 'departing':
                return have_some and self.activity == 'outbound'
            elif task == 'moving':
                return have_some and self.activity == 'transfer' and self.place.id != self.destination.id
            elif task == 'changing':
                return have_some and self.activity == 'adjust'
        return False
