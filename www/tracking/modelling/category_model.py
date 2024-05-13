#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.base_models import NamedBaseModel
from tracking.modelling.cardistry_models import name_is_key
from tracking.viewers.categories_viewer import CategoriesViewer


class Category(CupboardDisplayContextMixin, NamedBaseModel):
    """
    a Category is used to specify a Thing.
    It is shared by all the things and places of a Root.
    It belongs to one and only one Root.
    It has a collection of choices particular to it.
    Refinements are used to associate a Category with a Thing.
    """

    singular_label = 'Category'
    plural_label = 'Categories'
    possible_tasks = ['create', 'update', 'delete', 'add', 'remove']
    label_prefixes = {'create': 'Choice of '}
    flavor = "category"

    root_id = database.Column(database.Integer, database.ForeignKey('root.id'), nullable=False)
    choices = database.relationship('Choice', backref='category', lazy=True, cascade='all, delete')
    refinements = database.relationship('Refinement', backref='category', lazy=True, cascade='all, delete')
    unknown_specifics = database.relationship('UnknownSpecific', backref='category', lazy=True,
                                              cascade='all, delete')

    def viewable_children(self, viewer):
        return self.sorted_choices

    @property
    def parent_object(self):
        return CategoriesViewer(place=self.root.place, thing=self.root.thing)

    @property
    def identities(self):
        """ returns dictionary needed when constructing urls for category tasks """
        return {'category_id': self.id}

    def add_extra_actions(self, context, navigator, viewer, thing=None):
        if False and thing and self.may_update(viewer):  # TODO: fix this
            if self in thing.category_list:
                task = 'remove'
                preposition = 'from'
            else:
                task = 'add'
                preposition = 'to'
            self.add_task(context, navigator, task, label=f' {self.name} {preposition} {thing.name}')

    @property
    def sorted_choices(self):
        return sorted(self.choices, key=name_is_key)

    def create_choice(self, name, description):
        from tracking.modelling.choice_model import find_or_create_choice
        return find_or_create_choice(self, name, description)


def find_category_by_id(category_id):
    return category_id and Category.query.filter(Category.id == category_id).first()
