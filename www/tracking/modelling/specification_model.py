#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.modelling.base_models import IdModelMixin, DatedModelMixin
from tracking.modelling.cardistry_models import sorted_by_name
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


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

    @property
    def choice_label(self):
        choices = self.choices
        return (', ').join([f'{choice.name}' for choice in choices])

    @property
    def choices_insertion(self):
        label = self.choice_label
        if label:
            return f'{label} '
        else:
            return ''

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


def describe_choices(choices, unknowns=None):
    if unknowns:
        sorted_unknowns = sorted_by_name(unknowns)
        sorted_names = [f'Unknown {unknown.name}' for unknown in sorted_unknowns]
        suffix = ' ' + ' '.join(sorted_names)
    else:
        suffix = ''
    if choices:
        sorted_choices = sorted_by_name(choices)
        prefix =  (', ').join([f'{choice.name}' for choice in sorted_choices])
    else:
        prefix = 'Any'
    return f'{prefix}{suffix}'
