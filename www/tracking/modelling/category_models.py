#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from tracking import database
from tracking.cardistry.models.cardistry_models import name_is_key, bread_crumbs
from tracking.commons.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.base_models import IdModelMixin, NamedBaseModel


class Categories(CupboardDisplayContextMixin):
    label = 'Categories'
    singular_label = 'Categories'
    possible_tasks = []
    flavor = 'category'

    def __init__(self, root):
        self.root = root

    @property
    def identities(self):
        return {'root_id': self.root.id}

    @property
    def name(self):
        return self.label

    @property
    def parent_object(self):
        return self.root

    @property
    def root_path(self):
        return [self.root, self]

    def viewable_children(self, viewer):
        return [category for category in self.root.sorted_categories if category.may_be_observed(viewer)]

    def add_description(self, context):
        pass

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [self.root, self], target=self)


class Category(CupboardDisplayContextMixin, NamedBaseModel):
    singular_label = 'Category'
    plural_label = 'Categories'
    possible_tasks = []  # ['update', 'delete']
    label_prefixes = {}
    flavor = "category"

    root_id = database.Column(database.Integer, database.ForeignKey('root.id'), nullable=False)
    choices = database.relationship('Choice', backref='category', lazy=True, cascade='all, delete')
    refinements = database.relationship('Refinement', backref='category', lazy=True, cascade='all, delete')

    def viewable_children(self, viewer):
        return []

    @property
    def parent_object(self):
        return Categories(self.root)

    @property
    def identities(self):
        return {'category_id': self.id}

    def may_perform_task(self, viewer, task):
        if task == 'view':
            return self.may_be_observed(viewer)
        elif task == 'delete':
            return self.user_may_delete(viewer)
        elif task == 'update':
            return self.user_may_update(viewer)
        elif task == 'create':
            return self.user_may_create_choice(viewer)
        else:
            return False

    def may_be_observed(self, viewer):
        return True  # TODO: refine this

    def user_may_delete(self, viewer):
        return viewer.may_delete_category

    def user_may_update(self, viewer):
        return viewer.may_update_category

    def user_may_create_choice(self, viewer):
        # TODO: refine this
        return viewer.may_update_category

    @property
    def sorted_choices(self):
        return sorted(self.choices, key=name_is_key)


class Refinement(IdModelMixin, database.Model):
    category_id = database.Column(database.Integer, database.ForeignKey('category.id'))
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'))
    date_created = database.Column(database.DateTime(), default=datetime.now())


def find_category_by_id(id):
    return Category.query.filter(Category.id == id).first()


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
