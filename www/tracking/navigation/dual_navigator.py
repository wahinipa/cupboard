#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for

from tracking.modelling.category_models import Categories, Category
from tracking.modelling.choice_models import Choice
from tracking.modelling.place_model import Place
from tracking.modelling.root_model import Root
from tracking.modelling.thing_model import Thing
from tracking.navigation.navigator import navigational_mark


def root_url(root, place=None, thing=None, task='view'):
    if place is None:
        place = root.place
    if thing is None:
        thing = root.thing
    return url_for(f'root_bp.root_{task}', root_id=root.id, place_id=place.id, thing_id=thing.id)


class DualNavigator:
    def __init__(self, root=None, place=None, thing=None):
        from tracking.navigation.cupboard_navigation import create_cupboard_navigator
        self.navigator = create_cupboard_navigator()
        self.translator = {
            navigational_mark(Categories): self.categories_url,
            navigational_mark(Category): self.category_url,
            navigational_mark(Choice): self.choice_url,
            navigational_mark(Place): self.place_url,
            navigational_mark(Root): self.root_url,
            navigational_mark(Thing): self.thing_url,
        }
        if root is None:
            if place:
                root = place.root
            elif thing:
                root = thing.root
        if root:
            place = place or root.place
            thing = thing or root.thing
        self.root_id = root.id if root else None
        self.place_id = place.id if place else None
        self.thing_id = thing.id if thing else None

    def default_url(self, target, task):
        return self.navigator.url(target, task)

    def categories_url(self, categories, task):
        return url_for(f'categories_bp.categories_{task}', root_id=self.root_id, place_id=self.place_id,
                       thing_id=self.thing_id)

    def category_url(self, category, task):
        return url_for(f'category_bp.category_{task}', category_id=category.id, place_id=self.place_id,
                       thing_id=self.thing_id)

    def choice_url(self, choice, task):
        return url_for(f'choice_bp.choice_{task}', choice_id=choice.id, place_id=self.place_id, thing_id=self.thing_id)

    def place_url(self, place, task):
        if task == 'view':
            return self.root_url(place.root, task, place_id=place.id)
        url_for(f'place_bp.place_{task}', place_id=place.id, thing_id=self.thing_id)

    def root_url(self, root, task, place_id=None, thing_id=None):
        place_id = place_id or self.place_id or root.place.id
        thing_id = thing_id or self.thing_id or root.thing.id
        return url_for(f'root_bp.root_{task}', root_id=root.id, place_id=place_id, thing_id=thing_id)

    def thing_url(self, thing, task):
        if task == 'view':
            return self.root_url(thing.root, task, thing_id=thing.id)
        return url_for(f'thing_bp.thing_{task}', place_id=self.place_id, thing_id=thing.id)

    def url(self, target, task):
        return self.translator.get(navigational_mark(target), self.default_url)(target, task)
