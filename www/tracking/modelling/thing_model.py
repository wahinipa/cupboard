#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask import url_for
from sqlalchemy.orm import backref

from tracking import database
from tracking.modelling.base_models import RootDescendantMixin, NamedBaseModel
from tracking.modelling.cardistry_models import sorted_by_name
from tracking.viewing.cupboard_display_context import CupboardDisplayContextMixin


class Thing(RootDescendantMixin, CupboardDisplayContextMixin, NamedBaseModel):
    singular_label = "Thing"
    plural_label = "Things"
    possible_tasks = ['create', 'update', 'delete']
    label_prefixes = {'create': 'Kind of '}
    flavor = "thing"

    roots = database.relationship('Root', backref='thing', lazy=True)
    refinements = database.relationship('Refinement', backref='thing', lazy=True)

    kind_of_id = database.Column(database.Integer, database.ForeignKey('thing.id'), index=True)
    kinds = database.relationship('Thing', lazy='subquery', backref=backref('kind_of', remote_side='Thing.id'))

    @property
    def identities(self):
        return {'thing_id': self.id}

    @property
    def children(self):
        return self.kinds

    @property
    def sorted_categories(self):
        return sorted_by_name(self.category_list)

    @property
    def category_list(self):
        category_list = [refinement.category for refinement in self.refinements]
        if not self.is_top:
            for category in self.parent_object.category_list:
                if not category in category_list:
                    category_list.append(category)
        return category_list

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
    def parent_list(self):
        if self.is_top:
            return []
        else:
            return self.parent_object.parent_list + [self.parent_object]

    def local_category_refinements(self, category):
        return [refinement for refinement in self.refinements if refinement.category == category]

    def deep_category_refinements(self, category):
        refinements = []
        for thing in self.kinds:
            refinements += thing.local_category_refinements(category)
        return refinements

    def category_refinements(self, category):
        return self.local_category_refinements(category) + self.deep_category_refinements(category)

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
        return self.sorted_categories + self.sorted_children


def find_thing_by_id(thing_id):
    return Thing.query.filter(Thing.id == thing_id).first()
