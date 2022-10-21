#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for
from sqlalchemy.orm import backref

from tracking import database
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.base_models import UniqueNamedBaseModel, RootDescendantMixin


class Thing(RootDescendantMixin, CupboardDisplayContextMixin, UniqueNamedBaseModel):
    singular_label = "Thing"
    plural_label = "Things"
    possible_tasks = ['create', 'update', 'delete']
    label_prefixes = {'create': 'Kind of '}
    flavor="thing"

    roots = database.relationship('Root', backref='thing', lazy=True)
    # refinements = database.relationship('Root', backref='thing', lazy=True)

    kind_of_id = database.Column(database.Integer, database.ForeignKey('thing.id'), index=True)
    kinds = database.relationship('Thing', lazy='subquery', backref=backref('kind_of', remote_side='Thing.id'))

    @property
    def identities(self):
        return {'thing_id': self.id}

    @property
    def children(self):
        return self.kinds

    def create_kind_of_thing(self, name, description, date_created=None):
        if date_created is None:
            date_created = datetime.now()
        thing = Thing(name=name, description=description, kind_of=self, date_created=date_created)
        database.session.add(thing)
        database.session.commit()
        return thing

    def may_perform_task(self, viewer, task):
        if task == 'view':
            return self.may_be_observed(viewer)
        elif task == 'create':
            return self.may_create_thing(viewer)
        elif task == 'delete':
            return self.may_delete(viewer)
        elif task == 'update':
            return self.may_update(viewer)
        else:
            return False

    def may_be_observed(self, viewer):
        return self.ancestor.may_be_observed(viewer)

    def may_create_thing(self, viewer):
        return self.ancestor.may_create_thing(viewer)

    def may_delete(self, viewer):
        return self.ancestor.may_delete(viewer)

    def may_update(self, viewer):
        return self.ancestor.may_update(viewer)

    @property
    def page_template(self):
        return "pages/thing_view.j2"

    @property
    def parent_object(self):
        return self.kind_of

    @property
    def root(self):
        from tracking.modelling.root_model import thing_root
        return thing_root(self)

    @property
    def top_place(self):
        return self.root.place

    @property
    def url(self):
        return url_for('thing_bp.thing_view', thing_id=self.id)

    @property
    def url_create(self):
        return url_for('thing_bp.thing_create', thing_id=self.id)

    @property
    def url_delete(self):
        return url_for('thing_bp.thing_delete', thing_id=self.id)

    @property
    def url_update(self):
        return url_for('thing_bp.thing_update', thing_id=self.id)

    def viewable_children(self, viewer):
        return self.sorted_children


def find_thing_by_id(thing_id):
    return Thing.query.filter(Thing.id == thing_id).first()
