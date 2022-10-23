#  Copyright (c) 2022, Wahinipa LLC

class RootHolder:
    def __init__(self, place=None, thing=None, particular_thing=None):
        if place:
            root = place.root
        elif thing:
            root = thing.root
        else:
            root = None
        if root:
            place = place or root.place
            thing = thing or root.thing
        if thing and particular_thing is None:
            particular_thing = thing.generic

        self.root = root
        self.place = place
        self.thing = thing
        self.particular_thing = particular_thing

        self.root_id = root.id if root else None
        self.place_id = place.id if place else None
        self.thing_id = thing.id if thing else None
        self.particular_thing_id = particular_thing.id if particular_thing else None
