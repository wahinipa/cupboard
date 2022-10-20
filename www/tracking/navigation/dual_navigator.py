#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for

from tracking.modelling.category_models import Categories, Category
from tracking.modelling.choice_models import Choice
from tracking.modelling.place_model import Place
from tracking.modelling.root_model import Root
from tracking.modelling.thing_model import Thing
from tracking.navigation.navigator import navigational_mark


def root_url(root, place, thing):
    return url_for('root_bp.root_view', root_id=root.id, place_id=place.id, thing_id=thing.id)


def categories_url(root, place, thing):
    return url_for('categories_bp.categories_view', root_id=root.id, place_id=place.id, thing_id=thing.id)


def category_url(category, place, thing):
    return url_for('category_bp.category_view', category_id=category.id, place_id=place.id, thing_id=thing.id)


def category_url(category, place, thing, task='view'):
    return url_for(f'category_bp.category_{task}', category_id=category.id, place_id=place.id, thing_id=thing.id)


def choice_url(choice: object, place: object, thing: object, task: object = 'view') -> object:
    return url_for(f'choice_bp.choice_{task}', choice_id=choice.id, place_id=place.id, thing_id=thing.id)


class DualNavigator:
    def __init__(self, root=None, place=None, thing=None):
        from tracking.commons.cupboard_navigation import create_cupboard_navigator
        self.navigator = create_cupboard_navigator()
        self.root_mark = navigational_mark(Root)
        self.place_mark = navigational_mark(Place)
        self.thing_mark = navigational_mark(Thing)
        self.categories_mark = navigational_mark(Categories)
        self.category_mark = navigational_mark(Category)
        self.choice_mark = navigational_mark(Choice)

        self.root = root
        if place is None and root is not None:
            place = root.place
        self.place = place
        if thing is None and root is not None:
            thing = root.thing
        self.thing = thing

    def url(self, target, task):
        # TODO: simplify this mess. Dictionary? Mini classes?
        if task == 'view':
            if self.root is None:
                if navigational_mark(target) == self.root_mark:
                    return root_url(target, target.place, target.thing)
            else:
                if navigational_mark(target) == self.root_mark:
                    return root_url(target, self.place, self.thing)
                else:
                    if navigational_mark(target) == self.place_mark:
                        return root_url(self.root, target, self.thing)
                    elif navigational_mark(target) == self.thing_mark:
                        return root_url(self.root, self.place, target)
                    elif navigational_mark(target) == self.categories_mark:
                        return categories_url(self.root, self.place, self.thing)
                    elif navigational_mark(target) == self.category_mark:
                        return category_url(target, self.place, self.thing)
        if navigational_mark(target) == self.category_mark:
            return category_url(target, self.place, self.thing, task=task)
        elif navigational_mark(target) == self.choice_mark:
            return choice_url(target, self.place, self.thing, task=task)

        return self.navigator.url(target, task)
