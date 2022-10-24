#  Copyright (c) 2022, Wahinipa LLC

class Placement:
    def __init__(self, root=None, place=None, thing=None, specification=None):
        if root is None:
            if place:
                root = place.root
            elif thing:
                root = thing.root
            elif specification:
                root = specification.root
        if root:
            place = place or root.place
            thing = thing or root.thing
            specification = specification or root.generic_specification
        self.root = root
        self.place = place
        self.thing = thing
        self.specification = specification

    @property
    def is_valid(self):
        return self.root and self.thing and self.place and self.specification \
               and self.thing.root == self.root and self.place.root == self.root \
               and self.specification.root == self.root

    def may_be_observed(self, viewer):
        return self.is_valid and self.root.may_be_observed(viewer)




