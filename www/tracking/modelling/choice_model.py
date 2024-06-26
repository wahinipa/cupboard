#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.base_models import NamedBaseModel


class Choice(CupboardDisplayContextMixin, NamedBaseModel):
    """
    A choice belongs to a Category and is used in Specifications.
    For example "Winter Only" might be a Choice for the "Seasonal" Category
    and be used in any Specification that has "Winter Only" as part of it.
    """

    singular_label = 'Choice'
    plural_label = 'Choices'
    possible_tasks = ['update', 'delete']
    label_prefixes = {}
    flavor = "choice"

    # A Choice is part of only one Category
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'), nullable=False)

    # It is potentially included in multiple Specifications.
    specifications = database.relationship('Specific', backref='choice', lazy=True, cascade='all, delete')

    def viewable_children(self, viewer):
        return []

    @property
    def parent_object(self):
        return self.category

    @property
    def identities(self):
        """ returns dictionary needed when constructing urls for Choice tasks """
        return {'choice_id': self.id}

    @property
    def root(self):
        return self.category.root


def find_or_create_choice(category, name, description="", date_created=None):
    choice = find_choice(category, name)
    if choice is None:
        if date_created is None:
            date_created = datetime.now()
        choice = Choice(category=category, name=name, description=description, date_created=date_created)
        database.session.add(choice)
        database.session.commit()
    return choice


def find_choice(category, name):
    return Choice.query.filter(Choice.category_id == category.id, Choice.name == name).first()


def find_choice_by_id(choice_id):
    return choice_id and Choice.query.filter(Choice.id == choice_id).first()
