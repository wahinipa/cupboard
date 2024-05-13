#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.modelling.base_models import IdModelMixin


class Positioning(IdModelMixin, database.Model):
    """
    A Positioning is the core information record that says:
        How much (quantity)
        of what kind of object (Thing + Specification)
        is at a particular location (Place)
    """
    place_id = database.Column(database.Integer, database.ForeignKey('place.id'))
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'), index=True)
    specification_id = database.Column(database.Integer, database.ForeignKey('specification.id'), index=True)
    quantity = database.Column(database.Integer, nullable=False, server_default='0')

    @property
    def name(self):
        return f'{self.thing.name} at {self.place.name}'


def _find_positionings(place, thing, specification):
    return Positioning.query.filter(Positioning.place_id == place.id,
                                    Positioning.thing_id == thing.id,
                                    Positioning.specification_id == specification.id
                                    ).all()


def find_exact_quantity_of_things_at_place(place, thing, specification):
    return sum(positioning.quantity for positioning in _find_positionings(place, thing, specification))


def add_quantity_of_things(place, thing, specification, quantity, do_commit=True):
    requested_quantity = quantity + find_exact_quantity_of_things_at_place(place, thing, specification)
    return change_quantity_of_things(place, thing, specification, requested_quantity, do_commit=do_commit)

def change_quantity_of_things(place, thing, specification, requested_quantity, do_commit=True):
    positionings = _find_positionings(place, thing, specification)
    if len(positionings) == 0:
        positioning = Positioning(place=place, thing=thing, specification=specification, quantity=requested_quantity)
        database.session.add(positioning)
    else:
        positioning = positionings[0]
        positioning.quantity = requested_quantity
        for excess_positioning in positionings[1:]:
            database.session.delete(excess_positioning)
    if do_commit:
        database.session.commit()
    return requested_quantity


def move_quantity_of_things(destination_place, source_place, thing, specification, quantity):
    return (
        add_quantity_of_things(destination_place.place_model, thing, specification, quantity, do_commit=False),
        add_quantity_of_things(source_place, thing, specification, -quantity, do_commit=True),
    )
