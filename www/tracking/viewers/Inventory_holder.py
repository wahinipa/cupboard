#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.positioning_mixin import filtered_positionings


class InventoryHolder:
    def __init__(self, place, thing, specification, positionings=None):
        self.place = place
        self.thing = thing
        self.specification = specification
        self.set_of_places = place and self.place.full_set
        self.set_of_things = thing and self.thing.full_set
        if positionings is None:
            if place:
                positionings = self.place.full_positionings
            else:
                positionings = []
        self.positionings = filtered_positionings(positionings, places=self.set_of_places, things=self.set_of_things,
                                                  specification=self.specification)
        self.quantity = sum(positioning.quantity for positioning in self.positionings)

    def place_inventory(self, place):
        return create_inventory(place, self.thing, self.specification, positionings=self.positionings)


def create_inventory(place, thing, specification, positionings=None):
    return InventoryHolder(place, thing, specification, positionings=positionings)
