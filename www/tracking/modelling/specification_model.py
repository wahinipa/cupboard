#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.modelling.base_models import IdModelMixin, DatedModelMixin
from tracking.modelling.cardistry_models import sorted_by_name


class Specific(IdModelMixin, database.Model):
    specification_id = database.Column(database.Integer, database.ForeignKey('specification.id'), index=True)
    choice_id = database.Column(database.Integer, database.ForeignKey('choice.id'), index=True)


class UnknownSpecific(IdModelMixin, database.Model):
    specification_id = database.Column(database.Integer, database.ForeignKey('specification.id'), index=True)
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'), index=True)


class Specification(IdModelMixin, DatedModelMixin, database.Model):
    root_id = database.Column(database.Integer, database.ForeignKey('root.id'))
    specifics = database.relationship('Specific', backref='specification', lazy=True, cascade='all, delete')
    unknown_specifics = database.relationship('UnknownSpecific', backref='specification', lazy=True,
                                              cascade='all, delete')
    positionings = database.relationship('Positioning', backref='specification', lazy=True, cascade='all, delete')

    @property
    def name(self):
        return describe_choices(self.choices, self.unknowns)

    @property
    def choices(self):
        return {specific.choice for specific in self.specifics}

    @property
    def sorted_choices(self):
        return sorted_by_name(self.choices)

    @property
    def choice_categories(self):
        return {choice.category for choice in self.choices}

    @property
    def unknowns(self):
        return {unknown_specific.category for unknown_specific in self.unknown_specifics}

    @property
    def categories(self):
        return self.choice_categories | self.unknowns

    def selected_choices(self, categories):
        return {choice for choice in self.choices if choice.category in categories}

    def has_choice(self, choice):
        return choice in self.choices

    def choices_for(self, category):
        return {choice for choice in self.choices if choice.category == category}

    def accepts(self, target_specification):
        unknown_search_categories = self.unknowns
        choice_search_categories = self.choice_categories
        categories_of_concern = choice_search_categories | unknown_search_categories
        desired_choices = self.choices
        for category in categories_of_concern:
            target_choices = target_specification.selected_choices({category})
            if not target_choices:
                if category not in unknown_search_categories:
                    return False
            else:
                matching_choices = target_choices & desired_choices
                if not matching_choices:
                    return False
        return True

    def may_update(self, viewer):
        return self.root.may_be_observed(viewer)


def find_specification_by_id(specification_id):
    return Specification.query.filter(Specification.id == specification_id).first()


def describe_choices(choices=None, unknowns=None, specification=None):
    if unknowns is None:
        if specification:
            unknowns = specification.unknowns
        else:
            unknowns = set()
    if choices is None:
        if specification:
            choices = specification.choices
        else:
            choices = set()
    label_pieces = []
    categories_set = {choice.category for choice in choices} | unknowns
    categories = sorted_by_name(list(categories_set))
    for category in categories:
        sorted_choices = sorted_by_name([choice for choice in choices if choice.category == category])
        sorted_names = [choice.name for choice in sorted_choices]
        if category in unknowns:
            sorted_names.append(f'Unknown')
        choice_description = ' or '.join(sorted_names)
        label_pieces.append(f'{choice_description} {category.name}')
    full_label = ', '.join(label_pieces)
    if full_label:
        return full_label
    else:
        return 'All Choices'
