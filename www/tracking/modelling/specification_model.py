#  Copyright (c) 2022, Wahinipa LLC

from tracking import database
from tracking.modelling.base_models import IdModelMixin, DatedModelMixin


class Specific(IdModelMixin, database.Model):
    specification_id = database.Column(database.Integer, database.ForeignKey('specification.id'), index=True)
    choice_id = database.Column(database.Integer, database.ForeignKey('choice.id'), index=True)


class Specification(IdModelMixin, DatedModelMixin, database.Model):
    root_id = database.Column(database.Integer, database.ForeignKey('root.id'))
    specifics = database.relationship('Specific', backref='specification', lazy=True, cascade='all, delete')
    particular_things = database.relationship('ParticularThing', backref='specification', lazy=True)

    @property
    def choices(self):
        return {specific.choice for specific in self.specifics}

    def has_choice(self, choice):
        return choice in self.choices
