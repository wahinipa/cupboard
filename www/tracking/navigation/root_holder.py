#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.particular_thing_model import find_or_create_particular_thing


class RootHolder:
    def __init__(self, root=None, place=None, thing=None, specification=None, particular_thing=None):
        if particular_thing and specification is None:
            specification = particular_thing.specification
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

        if particular_thing and specification is None:
            specification = particular_thing.specification

        if thing and specification and particular_thing is None:
            particular_thing = find_or_create_particular_thing(thing, specification.choices)

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

        if particular_thing:
            self.particular_thing_id = particular_thing.id
        else:
            self.particular_thing_id = None

        self.root = root
        self.place = place
        self.thing = thing
        self.specification = specification
        self.particular_thing = particular_thing
