#  Copyright (c) 2022, Wahinipa LLC
from tracking import database
from tracking.modelling.base_models import IdModelMixin

class Particular(IdModelMixin, database.Model):
    particular_thing_id = database.Column(database.Integer, database.ForeignKey('particular_thing.id'), index=True)
    choice_id = database.Column(database.Integer, database.ForeignKey('choice.id'), index=True)


def _find_or_create_particular(particular_thing, choice):
    particular = particular_thing.find_particular(choice)
    if particular is None:
        particular = Particular(particular_thing=particular_thing, choice=choice)
        database.session.add(particular)
        # Do not commit yet, else database could be corrupted by duplicates.
    return particular

class ParticularThing(IdModelMixin, database.Model):
    thing_id = database.Column(database.Integer, database.ForeignKey('thing.id'), index=True)
    particulars = database.relationship('Particular', backref='particular_thing', lazy=True, cascade='all, delete')
    positionings = database.relationship('Positioning', backref='particular_thing', lazy=True, cascade='all, delete')

    @property
    def kind_of(self):
        return self.thing

    @property
    def choices(self):
        return [particular.choice for particular in self.particulars]

    def quantity_at_place(self, place):
        from tracking.modelling.postioning_model import find_quantity_of_things
        return find_quantity_of_things(place, self)

    def add_to_place(self, place, quantity):
        from tracking.modelling.postioning_model import add_quantity_of_things
        return add_quantity_of_things(place, self, quantity)

    def find_particular(self, choice):
        for particular in self.particulars:
            if particular.choice == choice:
                return particular
        return None


def find_or_create_particular_thing(thing, choices):
    particular_thing = find_particular_thing(thing, choices)
    if particular_thing is None:
        # Create ParticularThing...
        particular_thing = ParticularThing(thing=thing)
        database.session.add(particular_thing)
        for choice in choices:
            # ... and one Particular to capture each choice ...
            _find_or_create_particular(particular_thing, choice)
        # ... then commit the whole set into the database as a single transaction.
        database.session.commit()
    return particular_thing


def find_particular_thing(thing, choices):
    count = len(choices)

    def has_same_choices(particular_thing):
        possible_choices = particular_thing.choices
        if len(possible_choices) != count:
            return False
        else:
            for choice in choices:
                if choice not in possible_choices:
                    return False
            return True

    for particular_thing in thing.particular_things:
        if has_same_choices(particular_thing):
            return particular_thing
    return None
