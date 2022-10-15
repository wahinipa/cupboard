#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for

from tracking.modelling.place_model import Place
from tracking.modelling.root_model import Root
from tracking.modelling.thing_model import Thing
from tracking.navigation.navigator import navigational_mark


def root_url(root, place, thing):
    return url_for('root_bp.root_view', root_id=root.id, place_id=place.id, thing_id=thing.id)


class DualNavigator:
    def __init__(self, root=None, place=None, thing=None):
        from tracking.commons.cupboard_navigation import create_cupboard_navigator
        self.navigator = create_cupboard_navigator()
        self.root_mark = navigational_mark(Root)
        self.place_mark = navigational_mark(Place)
        self.thing_mark = navigational_mark(Thing)

        self.root = root
        self.place = place
        self.thing = thing

    def url(self, target, task):
        if task == 'view':
            if navigational_mark(target) == self.root_mark:
                return root_url(target, target.place, target.thing)
            elif self.root is not None:
                if navigational_mark(target) == self.place_mark and self.thing is not None:
                    return root_url(self.root, target, self.thing)
                elif navigational_mark(target) == self.thing_mark and self.place is not None:
                    return root_url(self.root, self.place, target)
        return self.navigator.url(target, task)
