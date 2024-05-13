#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.modelling.base_models import IdModelMixin, DatedModelMixin


class Refinement(IdModelMixin, DatedModelMixin, database.Model):
    """
    A Refinement associates a Category with a Thing.
    For example a seasonal Category might be associated with Clothing but not Toothpaste.
    """
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'))
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'))


def add_refinement(thing, category, date_created=None, commit=True):
    refinement = find_refinement(thing, category)
    if refinement is None:
        if date_created is None:
            date_created = datetime.now()
        lower_refinements = thing.category_refinements(category)
        refinement = Refinement(thing=thing, category=category, date_created=date_created)
        database.session.add(refinement)
        for lower_refinement in lower_refinements:
            database.session.delete(lower_refinement)
        if commit:
            database.session.commit()
    return refinement


def remove_refinement(thing, category, date_created=None):
    if date_created is None:
        date_created = datetime.now()
    removals = []
    refinement = find_refinement(thing, category)
    if refinement is not None:
        removals.append(refinement)
    parents = thing.parent_list
    parents.reverse()
    removals += thing.category_refinements(category)
    for parent in parents:
        for parent_refinement in parent.local_category_refinements(category):
            # Push parent level refinement into all siblings of thing in chain.
            removals.append(parent_refinement)
            for child in parent.kinds:
                if child != thing:
                    add_refinement(child, category, date_created=date_created, commit=False)
        thing = parent
    for item in removals:
        database.session.delete(item)
    database.session.commit()


def find_refinement(thing, category):
    for refinement in thing.refinements:
        if refinement.category_id == category.id:
            return refinement
    return None
