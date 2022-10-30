#  Copyright (c) 2022, Wahinipa LLC

class PositioningMixin:
    @property
    def direct_positionings(self):
        return set(self.positionings)

    @property
    def full_positionings(self):
        full_positionings = self.direct_positionings
        for child in self.children:
            full_positionings |= child.full_positionings
        return full_positionings


def current_quantity(place, thing, specification):
    total = 0
    for positioning in place.direct_positionings:
        if positioning.thing == thing and specification.accepts(positioning.specification):
            quantity = positioning.quantity
            if quantity > 0:
                total += quantity
    return total


def filtered_positioning_sum(positionings, places=None, things=None, specification=None):
    return sum_of_positioning_quantities(
        filtered_positionings(positionings=positionings, places=places, things=things, specification=specification))


def filtered_positionings(positionings, places=None, things=None, specification=None):
    return {
        position for position in positionings
        if (places is None or position.place in places)
           and (things is None or position.thing in things)
           and (specification is None or specification.accepts(position.specification))
    }


def sum_of_positioning_quantities(positionings):
    return sum(positioning.quantity for positioning in positionings)
