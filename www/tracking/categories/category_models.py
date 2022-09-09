#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.commons.base_models import UniqueNamedBaseModel, IdModelMixin


class Category(UniqueNamedBaseModel):
    choices = database.relationship('Choice', backref='category', lazy=True, cascade='all, delete')
    refinements = database.relationship('Refinement', backref='category', lazy=True, cascade='all, delete')


class Refinement(IdModelMixin, database.Model):
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'))
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'))
    date_created = database.Column(database.DateTime(), default=datetime.now())


def find_or_create_category(name, description="", date_created=None):
    category = find_category_by_name(name)
    if category is None:
        if date_created is None:
            date_created = datetime.now()
        category = Category(name=name, description=description, date_created=date_created)
        database.session.add(category)
        database.session.commit()
    return category


def find_category_by_name(name):
    return Category.query.filter(Category.name == name).first()


def refine_thing(thing, category, date_created=None):
    refinement = find_refinement(thing, category)
    if refinement is None:
        if date_created is None:
            date_created = datetime.now()
        refinement = Refinement(thing=thing, category=category, date_created=date_created)
        database.session.add(refinement)
        database.session.commit()
    return refinement


def find_refinement(thing, category):
    for refinement in thing.refinements:
        if refinement.category_id == category.id:
            return refinement
    return None