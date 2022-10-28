#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.specification_model import describe_choices
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


class CategorySpecification(CupboardDisplayContextMixin):
    plural_label = 'Choices'
    possible_tasks = []
    label_prefixes = {}
    flavor = "category_specification"
    def __init__(self, category, specification):
        self.category = category
        self.specification = specification
        self.choices = specification.choices_for(category)
        if category in specification.unknowns:
            self.unknowns = {category}
        else:
            self.unknowns = set()

    @property
    def singular_label(self):
        return f'{self.category.name} Choices'

    @property
    def name(self):
        return describe_choices(self.choices, self.unknowns)
