#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for
from sqlalchemy.orm import backref

from tracking import database
from tracking.modelling.base_models import NamedBaseModel


class Place(NamedBaseModel):
    singular_label = "Place"
    plural_label = "Places"

    roots = database.relationship('Root', backref='place', lazy=True)

    place_id = database.Column(database.Integer, database.ForeignKey('place.id'), index=True)
    places = database.relationship('Place', lazy='subquery', backref=backref('place_of', remote_side='Place.id'))

    @property
    def parent_object(self):
        return self.place_of

    @property
    def url(self):
        return url_for('place_bp.place_view', place_id=self.id)

    @property
    def root(self):
        from tracking.modelling.root_model import place_root
        return place_root(self)

    @property
    def top_thing(self):
        return self.root.thing

    def create_kind_of_place(self, name, description, date_created=None):
        if date_created is None:
            date_created = datetime.now()
        place = Place(name=name, description=description, place_of=self, date_created=date_created)
        database.session.add(place)
        database.session.commit()
        return place
