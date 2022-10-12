#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for
from sqlalchemy.orm import backref

from tracking import database
from tracking.commons.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.base_models import NamedBaseModel, RootDescendantMixin


class Place(RootDescendantMixin, CupboardDisplayContextMixin, NamedBaseModel):
    singular_label = "Place"
    plural_label = "Places"

    roots = database.relationship('Root', backref='place', lazy=True)

    place_id = database.Column(database.Integer, database.ForeignKey('place.id'), index=True)
    places = database.relationship('Place', lazy='subquery', backref=backref('place_of', remote_side='Place.id'))

    def add_additional_tasks(self, context, viewer):
        if self.may_create_place(viewer):
            context.add_task(self.url_create, label=f'Place of {self.name}', task='create')

    @property
    def classification(self):
        return 'Place'

    @property
    def children(self):
        return self.places

    def create_kind_of_place(self, name, description, date_created=None):
        if date_created is None:
            date_created = datetime.now()
        place = Place(name=name, description=description, place_of=self, date_created=date_created)
        database.session.add(place)
        database.session.commit()
        return place

    def may_be_observed(self, viewer):
        return self.ancestor.may_be_observed(viewer)

    def may_create_place(self, viewer):
        return self.ancestor.may_create_place(viewer)

    def may_delete(self, viewer):
        return self.ancestor.may_delete(viewer)

    def may_update(self, viewer):
        return self.ancestor.may_update(viewer)

    @property
    def page_template(self):
        return "pages/place_view.j2"

    @property
    def parent_object(self):
        return self.place_of

    @property
    def root(self):
        from tracking.modelling.root_model import place_root
        return place_root(self)

    @property
    def top_thing(self):
        return self.root.thing

    @property
    def url(self):
        return url_for('place_bp.place_view', place_id=self.id)

    @property
    def url_create(self):
        return url_for('place_bp.place_create', place_id=self.id)

    @property
    def url_delete(self):
        return url_for('place_bp.place_delete', place_id=self.id)

    @property
    def url_update(self):
        return url_for('place_bp.place_update', place_id=self.id)

    def viewable_children(self, viewer):
        return self.sorted_children


def find_place_by_id(place_id):
    return Place.query.filter(Place.id == place_id).first()
