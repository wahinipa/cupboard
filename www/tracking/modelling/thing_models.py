#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from sqlalchemy.orm import backref

from tracking import database
from tracking.modelling.base_models import UniqueNamedBaseModel


class Thing(UniqueNamedBaseModel):
    singular_label = "Thing"
    plural_label = "Things"

    roots = database.relationship('Root', backref='thing', lazy=True)

    kind_of_id = database.Column(database.Integer, database.ForeignKey('thing.id'), index=True)
    kinds = database.relationship('Thing', lazy='subquery', backref=backref('kind_of', remote_side='Thing.id'))

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

    def create_kind_of_thing(self, name, description, date_created=None):
        if date_created is None:
            date_created = datetime.now()
        thing = Thing(name=name, description=description, kind_of=self, date_created=date_created)
        database.session.add(thing)
        database.session.commit()
        return thing
