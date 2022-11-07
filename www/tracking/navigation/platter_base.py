#  Copyright (c) 2022, Wahinipa LLC


DEFAULT_ACTIVITY = 'observe'

class PlatterBase:
    def __init__(self, activity=DEFAULT_ACTIVITY, root=None, place=None, thing=None, specification=None):
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
            self.root_id = root.id
        else:
            self.root_id = None

        if place:
            self.place_id = place.id
        else:
            self.place_id = None

        if thing:
            self.thing_id = thing.id
        else:
            self.thing_id = None

        if specification:
            self.specification_id = specification.id
        else:
            self.specification_id = None

        self.activity = activity
        self.root = root
        self.place = place
        self.thing = thing
        self.specification = specification
