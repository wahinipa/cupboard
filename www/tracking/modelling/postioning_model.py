#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.modelling.base_models import IdModelMixin


class Positioning(IdModelMixin, database.Model):
    place_id = database.Column(database.Integer, database.ForeignKey('place.id'))
    particular_thing_id = database.Column(database.Integer, database.ForeignKey('particular_thing.id'))
    quantity = database.Column(database.Integer, nullable=False, server_default='0')


def _find_positionings(place, particular_thing):
    # return [positioning fo]
    return Positioning.query.filter(Positioning.place_id == place.id,
                                    Positioning.particular_thing_id == particular_thing.id).all()


def find_exact_quantity_of_things_at_place(place, particular_thing):
    return sum(positioning.quantity for positioning in _find_positionings(place, particular_thing))


def add_quantity_of_things(place, particular_thing, quantity):
    requested_quantity = quantity + find_exact_quantity_of_things_at_place(place, particular_thing)
    positionings = _find_positionings(place, particular_thing)
    if len(positionings) == 0:
        positioning = Positioning(place=place, particular_thing=particular_thing, quantity=quantity)
        database.session.add(positioning)
    else:
        positioning = positionings[0]
        positioning.quantity = requested_quantity
        for excess_positioning in positionings[1:]:
            database.session.delete(excess_positioning)
    database.session.commit()
    return requested_quantity


def move_quantity_of_things(destination_place, source_place, particular_thing, quantity):
    return (
        add_quantity_of_things(destination_place, particular_thing, quantity),
        add_quantity_of_things(source_place, particular_thing, -quantity),
    )
