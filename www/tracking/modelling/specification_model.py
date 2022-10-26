#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.modelling.base_models import IdModelMixin, DatedModelMixin


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
    particular_things = database.relationship('ParticularThing', backref='specification', lazy=True)

    @property
    def choices(self):
        return {specific.choice for specific in self.specifics}

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


def find_specification_by_id(specification_id):
    return Specification.query.filter(Specification.id == specification_id).first()
