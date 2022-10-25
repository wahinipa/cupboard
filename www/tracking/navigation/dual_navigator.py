#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for

from tracking.modelling.categories_model import Categories
from tracking.modelling.category_model import Category
from tracking.modelling.choice_model import Choice
from tracking.modelling.particular_thing_model import ParticularThing
from tracking.modelling.place_model import Place
from tracking.modelling.root_model import Root
from tracking.modelling.thing_model import Thing
from tracking.navigation.navigator import navigational_mark
from tracking.navigation.root_holder import RootHolder


def root_url(root, place=None, particular_thing=None, task='view'):
    if place is None:
        place = root.place
    if particular_thing is None:
        particular_thing = root.generic
    return url_for(f'root_bp.root_{task}', root_id=root.id, place_id=place.id, particular_thing=particular_thing.id)


class DualNavigator(RootHolder):
    def __init__(self, root=None, place=None, thing=None, specification=None, particular_thing=None):
        super().__init__(root=root, place=place, thing=thing, specification=specification,
                         particular_thing=particular_thing)
        from tracking.navigation.cupboard_navigation import create_cupboard_navigator
        self.navigator = create_cupboard_navigator()
        self.translator = {
            navigational_mark(Categories): self.categories_url,
            navigational_mark(Category): self.category_url,
            navigational_mark(Choice): self.choice_url,
            navigational_mark(Place): self.place_url,
            navigational_mark(Root): self.root_url,
            navigational_mark(Thing): self.thing_url,
            navigational_mark(ParticularThing): self.particular_thing_url,
        }

    def default_url(self, target, task):
        return self.navigator.url(target, task)

    def categories_url(self, categories, task):
        return url_for(f'categories_bp.categories_{task}', place_id=self.place_id,
                       thing_id=self.thing_id, specification_id=self.specification_id)

    def category_url(self, category, task):
        if task in ['add', 'remove']:
            return self.refinement_url(category, task)
        else:
            return url_for(f'category_bp.category_{task}', category_id=category.id, place_id=self.place_id,
                           thing_id=self.thing_id, specification_id=self.specification_id)

    def choice_url(self, choice, task):
        return url_for(f'choice_bp.choice_{task}', choice_id=choice.id,
                       place_id=self.place_id, particular_thing_id=self.particular_thing_id)

    def place_url(self, place, task):
        if task == 'view':
            return self.root_url(place.root, task, place_id=place.id)
        return url_for(f'place_bp.place_{task}', place_id=place.id, thing_id=self.thing_id,
                       specification_id=self.specification_id)

    def refinement_url(self, category, task):
        return url_for(f'refinement_bp.refinement_{task}', category_id=category.id, place_id=self.place_id,
                       particular_thing_id=self.particular_thing_id)

    def root_url(self, root, task, place_id=None, thing_id=None, specification_id=None):
        place_id = place_id or self.place_id or root.place.id
        thing_id = thing_id or self.thing_id or root.thing.id
        specification_id = specification_id or self.specification_id or root.generic_specification.id
        return url_for(f'root_bp.root_{task}', place_id=place_id, thing_id=thing_id, specification_id=specification_id)

    def thing_url(self, thing, task):
        if task == 'view':
            return self.root_url(thing.root, task, thing_id=thing.id)
        return url_for(f'thing_bp.thing_{task}', place_id=self.place_id, particular_thing_id=thing.id)

    def particular_thing_url(self, particular_thing, task):
        if task == 'view':
            return self.root_url(particular_thing.root, task, thing_id=particular_thing.thing.id,
                                 specification_id=particular_thing.specification.id)
        return url_for(f'thing_bp.thing_{task}', place_id=self.place_id, particular_thing_id=particular_thing.id)

    def url(self, target, task):
        return self.translator.get(navigational_mark(target), self.default_url)(target, task)
