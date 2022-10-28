#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.modelling.base_models import IdModelMixin


class Positioning(IdModelMixin, database.Model):
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


def add_quantity_of_things(place, thing, specification, quantity):
    requested_quantity = quantity + find_exact_quantity_of_things_at_place(place, thing, specification)
    positionings = _find_positionings(place, thing, specification)
    if len(positionings) == 0:
        positioning = Positioning(place=place, thing=thing, specification=specification, quantity=quantity)
        database.session.add(positioning)
    else:
        positioning = positionings[0]
        positioning.quantity = requested_quantity
        for excess_positioning in positionings[1:]:
            database.session.delete(excess_positioning)
    database.session.commit()
    return requested_quantity


def move_quantity_of_things(destination_place, source_place, thing, specification, quantity):
    return (
        add_quantity_of_things(destination_place, thing, specification, quantity),
        add_quantity_of_things(source_place, thing, specification, -quantity),
    )
