#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.modelling.base_models import NamedBaseModel
from tracking.modelling.cardistry_models import name_is_key
from tracking.modelling.categories_model import Categories
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


class Category(CupboardDisplayContextMixin, NamedBaseModel):
    singular_label = 'Category'
    plural_label = 'Categories'
    possible_tasks = ['create', 'update', 'delete']
    label_prefixes = {'create': 'Choice of '}
    flavor = "category"

    root_id = database.Column(database.Integer, database.ForeignKey('root.id'), nullable=False)
    choices = database.relationship('Choice', backref='category', lazy=True, cascade='all, delete')
    refinements = database.relationship('Refinement', backref='category', lazy=True, cascade='all, delete')

    def viewable_children(self, viewer):
        return [choice for choice in self.sorted_choices if choice.may_be_observed(viewer)]

    @property
    def parent_object(self):
        return Categories(place=self.root.place, thing=self.root.thing)

    @property
    def identities(self):
        return {'category_id': self.id}

    def may_perform_task(self, viewer, task):
        if task == 'view':
            return self.may_be_observed(viewer)
        elif task == 'delete':
            return self.may_delete(viewer)
        elif task == 'update':
            return self.may_update(viewer)
        elif task == 'create':
            return self.may_create_choice(viewer)
        else:
            return False

    def add_extra_actions(self, context, navigator, viewer, thing=None):
        if thing and self.may_update(viewer):
            if self in thing.category_list:
                task = 'remove'
                preposition = 'from'
            else:
                task = 'add'
                preposition = 'to'
            self.add_task(context, navigator, task, label=f' {self.name} {preposition} {thing.name}')

    def may_be_observed(self, viewer):
        return True  # TODO: refine this

    def may_delete(self, viewer):
        return viewer.may_delete_category

    def may_update(self, viewer):
        return viewer.may_update_category

    def may_create_choice(self, viewer):
        # TODO: refine this
        return viewer.may_update_category

    @property
    def sorted_choices(self):
        return sorted(self.choices, key=name_is_key)

    def create_choice(self, name, description):
        from tracking.modelling.choice_model import find_or_create_choice
        return find_or_create_choice(self, name, description)


def find_category_by_id(id):
    return Category.query.filter(Category.id == id).first()
