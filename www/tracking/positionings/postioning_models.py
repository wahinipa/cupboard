#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.commons.base_models import IdModelMixin


class Positioning(IdModelMixin, database.Model):
    place_id = database.Column(database.Integer, database.ForeignKey('place.id'))
    particular_thing_id = database.Column(database.Integer, database.ForeignKey('particular_thing.id'))
    quantity = database.Column(database.Integer, nullable=False, server_default='0')


def _find_positionings(place, particular_thing_id):
    return Positioning.query.filter(Positioning.place_id == place.id, Positioning.particular_thing_id == particular_thing_id.id).all()


def find_quantity_of_things(place, particular_thing):
    sum = 0
    for positioning in _find_positionings(place, particular_thing):
        sum += positioning.quantity
    return sum


def add_quantity_of_things(place, particular_thing, quantity):
    total_quantity = quantity
    positionings = _find_positionings(place, particular_thing)
    for positioning in positionings:
        total_quantity += positioning.quantity
    if len(positionings) == 0:
        positioning = Positioning(place=place, particular_thing=particular_thing, quantity=quantity)
        database.session.add(positioning)
    else:
        positioning = positionings[0]
        positioning.quantity = total_quantity
        for excess_positioning in positionings[1:]:
            database.session.delete(excess_positioning)
    database.session.commit()
    return total_quantity
