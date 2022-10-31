#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.cardistry_models import sorted_by_name
from tracking.modelling.category_specification import CategorySpecification
from tracking.modelling.specification_model import describe_choices
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin


class ThingSpecification(CupboardDisplayContextMixin):
    flavor = 'specification'
    label = 'Specification'
    label_prefixes = {}
    singular_label = 'Specification'
    possible_tasks = []

    def __init__(self, thing, specification):
        self.thing = thing
        self.specification = specification
        self.thing_categories = thing.complete_set_of_categories
        self.choices = {choice for choice in specification.choices if choice.category in self.thing_categories}
        self.unknowns = {unknown for unknown in specification.unknowns if unknown in self.thing_categories}

    def add_description(self, context):
        pass

    def choices_for(self, category):
        return {choice for choice in self.choices if choice.category == category}

    @property
    def is_specific(self):
        found_categories = self.unknowns
        for choice in self.choices:
            category = choice.category
            if category in found_categories:
                return False  # multiple choices for this category
            found_categories.add(category)
        return found_categories == self.thing_categories

    @property
    def name(self):
        return describe_choices(self.choices, self.unknowns)

    def viewable_children(self, viewer):
        sorted_categories = sorted_by_name(list(self.thing.complete_set_of_categories))
        return [CategorySpecification(category, self) for category in sorted_categories]
