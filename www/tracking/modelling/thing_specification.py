#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.category_specification import CategorySpecification
from tracking.modelling.specification_model import describe_choices
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


class ThingSpecification(CupboardDisplayContextMixin):
    flavor = 'specification'
    label = 'Specification'
    label_prefixes = {}
    singular_label = 'Specification'
    possible_tasks = []

    def __init__(self, thing, specification):
        self.thing = thing
        self.specification = specification
        thing_categories = set(thing.category_list)
        self.choices = {choice for choice in specification.choices if choice.category in thing_categories}

    def add_description(self, context):
        pass

    def choices_for(self, category):
        return {choice for choice in self.choices if choice.category == category}

    @property
    def name(self):
        return describe_choices(self.choices)

    def viewable_children(self, viewer):
        return [CategorySpecification(category, self) for category in self.thing.sorted_categories]
