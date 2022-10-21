#  Copyright (c) 2022, Wahinipa LLC

class RootHolder:
    def __init__(self, place=None, thing=None):
        if place:
            root = place.root
        elif thing:
            root = thing.root
        else:
            root = None
        if root:
            place = place or root.place
            thing = thing or root.thing
        self.root = root
        self.place = place
        self.thing = thing
        self.root_id = root.id if root else None
        self.place_id = place.id if place else None
        self.thing_id = thing.id if thing else None
