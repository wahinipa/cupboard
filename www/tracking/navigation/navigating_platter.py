#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for

from tracking.modelling.category_model import Category
from tracking.modelling.choice_model import Choice
from tracking.modelling.place_model import Place
from tracking.modelling.root_model import Root
from tracking.modelling.thing_model import Thing
from tracking.navigation.navigator import navigational_mark
from tracking.navigation.platter_base import PlatterBase, DEFAULT_ACTIVITY
from tracking.viewers.categories_viewer import CategoriesViewer
from tracking.viewers.category_specification_viewer import CategorySpecificationViewer
from tracking.viewers.destination import Destination


class NavigatingPlatter(PlatterBase):
    def __init__(self, **kwargs):
        PlatterBase.__init__(self, **kwargs)
        from tracking.navigation.cupboard_navigation import create_cupboard_navigator
        self.navigator = create_cupboard_navigator()
        self.translator = {
            navigational_mark(CategoriesViewer): self.categories_url_maker,
            navigational_mark(Category): self.category_url_maker,
            navigational_mark(Choice): self.choice_url_maker,
            navigational_mark(Destination): self.destination_url_maker,
            navigational_mark(Place): self.place_url_maker,
            navigational_mark(Root): self.root_url_maker,
            navigational_mark(CategorySpecificationViewer): self.specification_url_maker,
            navigational_mark(Thing): self.thing_url_maker,
        }

    def default_url_maker(self, target, task, activity=None):
        return self.navigator.url(target, task)

    def categories_url_maker(self, categories, task, activity=None):
        return url_for(f'categories_bp.categories_{task}', activity=activity, place_id=self.place_id,
                       destination_id=self.destination_id,
                       thing_id=self.thing_id, specification_id=self.specification_id)

    def category_url_maker(self, category, task, activity=None):
        if task in ['add', 'remove']:
            return self.refinement_url_maker(category, task, activity=activity)
        else:
            return url_for(f'category_bp.category_{task}', category_id=category.id, activity=activity,
                           destination_id=self.destination_id,
                           place_id=self.place_id, thing_id=self.thing_id, specification_id=self.specification_id)

    def choice_url_maker(self, choice, task, activity=None):
        return url_for(f'choice_bp.choice_{task}', choice_id=choice.id, activity=activity, place_id=self.place_id,
                       destination_id=self.destination_id,
                       thing_id=self.thing_id, specification_id=self.specification_id)

    def place_url_maker(self, place, task, activity=None):
        if task == 'view':
            return self.root_url_maker(place.root, task, place_id=place.id, activity=activity)
        return url_for(f'place_bp.place_{task}', activity=activity, place_id=place.id, thing_id=self.thing_id,
                       destination_id=self.destination_id,
                       specification_id=self.specification_id)

    def destination_url_maker(self, destination, task, activity=None):
        return self.root_url_maker(destination.root, 'view', destination_id=destination.id, activity=activity)

    def refinement_url_maker(self, category, task, activity=None):
        return url_for(f'refinement_bp.refinement_{task}', category_id=category.id, activity=activity,
                       destination_id=self.destination_id,
                       place_id=self.place_id, thing_id=self.thing_id, specification_id=self.specification_id)

    def root_url_maker(self, root, task, place_id=None, thing_id=None, specification_id=None, activity=None, destination_id=None):
        place_id = place_id or self.place_id or root.place.id
        destination_id = destination_id or self.destination_id or root.place.id
        thing_id = thing_id or self.thing_id or root.thing.id
        specification_id = specification_id or self.specification_id or root.generic_specification.id
        return url_for(f'root_bp.root_{task}', activity=activity, place_id=place_id, thing_id=thing_id,
                       destination_id=destination_id,
                       specification_id=specification_id)

    def specification_url_maker(self, category_specification, task, activity=None):
        # No matter the presumed task, do an update
        return url_for(f'specification_bp.specification_update', category_id=category_specification.category.id,
                       activity=activity, place_id=self.place_id, thing_id=self.thing_id,
                       destination_id=self.destination_id,
                       specification_id=self.specification_id)

    def thing_url_maker(self, thing, task, activity=None):
        if task == 'view':
            return self.root_url_maker(thing.root, task, thing_id=thing.id, activity=activity)
        return url_for(f'thing_bp.thing_{task}', activity=activity, place_id=self.place_id, thing_id=self.thing_id,
                       destination_id=self.destination_id,
                       specification_id=self.specification_id)

    def url(self, target, task, activity=None):
        activity = activity or self.activity or DEFAULT_ACTIVITY
        return self.translator.get(navigational_mark(target), self.default_url_maker)(target, task, activity=activity)
