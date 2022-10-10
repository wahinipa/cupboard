#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.modelling.base_models import UniqueNamedBaseModel


class Root(UniqueNamedBaseModel):
    singular_label = "Root"
    plural_label = "Roots"

    place_id = database.Column(database.Integer, database.ForeignKey('place.id'), unique=True, nullable=False)
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'), unique=True, nullable=False)


def place_root(place):
    top = place.top
    return Root.query.filter(Root.place_id == top.id).first()


def thing_root(thing):
    top = thing.top
    return Root.query.filter(Root.thing_id == top.id).first()

def create_root(name, description):
    from tracking.modelling.place_models import Place
    place_name = f'All {name} Places'
    place_description = f'All the top places for {name}'
    place = Place(name=place_name, description=place_description)
    database.session.add(place)

    from tracking.modelling.thing_models import Thing
    thing_name = f'All {name} Things'
    thing_description = f'All the top things for {name}'
    thing = Thing(name=thing_name, description=thing_description)
    database.session.add(thing)

    root = Root(name=name, description=description, place=place, thing=thing)
    database.session.add(root)
    database.session.commit()

    return root


