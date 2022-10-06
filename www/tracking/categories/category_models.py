#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for

from tracking import database
from tracking.commons.base_models import IdModelMixin, UniqueNamedBaseModel, name_is_key
from tracking.commons.display_context import DisplayContext
from tracking.commons.pseudo_model import PseudoModel
from tracking.commons.text_utilities import description_notation_list


class AllCategories(PseudoModel):
    def __init__(self, home):
        super().__init__(
            label="Categories",
            endpoint='category_bp.category_list',
            description="Categories are lists of Choices for being more specific about Things",
            parent_object=home
        )

    def may_be_observed(self, viewer):
        return viewer.may_observe_categories

    @property
    def child_list(self):
        return sorted(Category.query.all(), key=name_is_key)

    def add_actions(self, context, viewer):
        if viewer.may_create_category:
            context.add_action(url_for('category_bp.category_create'), 'Category', 'create')
        return context.display_context


class Category(UniqueNamedBaseModel):
    choices = database.relationship('Choice', backref='category', lazy=True, cascade='all, delete')
    refinements = database.relationship('Refinement', backref='category', lazy=True, cascade='all, delete')

    @property
    def parent_list(self):
        from tracking.home.home_models import home_root
        return [home_root, home_root.all_categories]

    def viewable_attributes(self, viewer):
        notations = self.description_notation_list
        choices = self.choices
        if choices:
            notations.append({
                'label': "Choices"
            })
            for choice in choices:
                notations += description_notation_list(tag=choice.name, description=choice.description)

        return {
            'classification': 'Category',
            'name': self.name,
            'label': self.label,
            'view_url': self.url,
            'notations': notations,
        }

    def display_context(self, viewer):
        category_context = DisplayContext({
            'target': self.viewable_attributes(viewer),
            'name': self.name,
            'label': self.label,
            'parent_list': self.parent_list,
            'children': [choice.viewable_attributes(viewer) for choice in self.sorted_choices]
        })
        if self.user_may_create_choice(viewer):
            category_context.add_action(self.place_create_url, f'Choice for {self.name}', 'create')
        if viewer.may_update_category:
            category_context.add_action(self.update_url, self.name, 'update')
        if viewer.may_delete_category:
            category_context.add_action(self.deletion_url, self.name, 'delete')
        return category_context

    def may_be_observed(self, user):
        return True  # TODO: refine this

    def user_may_delete(self, user):
        return user.may_delete_category

    def user_may_update(self, user):
        return user.may_update_category

    def user_may_create_choice(self, user):
        # TODO: refine this
        return user.may_update_category

    @property
    def sorted_choices(self):
        return sorted(self.choices, key=name_is_key)

    @property
    def url(self):
        return url_for('category_bp.category_view', category_id=self.id)

    @property
    def deletion_url(self):
        return url_for('category_bp.category_delete', category_id=self.id)

    @property
    def update_url(self):
        return url_for('category_bp.category_update', category_id=self.id)

    @property
    def place_create_url(self):
        return url_for('category_bp.choice_create', category_id=self.id)


def category_list_display_context(viewer):
    category_context = DisplayContext({
        'tab': 'category',
        'label': 'Categories',
        'name': 'Categories',
        'categories': viewer.viewable_categories,
    })
    if viewer.may_create_category:
        category_context.add_action(url_for('category_bp.category_create'), 'Category', 'create')
    return category_context.display_context


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


def all_categories():
    return sorted(Category.query.all(), key=name_is_key)
