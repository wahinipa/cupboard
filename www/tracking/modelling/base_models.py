#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from sqlalchemy.orm import declared_attr

from tracking.cardistry.models.cardistry_models import NamedMixin, DescribedMixin, HierarchicalMixin
from tracking import database


class IdModelMixin():
    @declared_attr
    def id(cls):
        return database.Column(database.Integer, primary_key=True)

    @property
    def unique_id(self):
        return f'{self.__class__.__name__}_{self.id}'


class NamedModelMixin(NamedMixin):
    @declared_attr
    def name(cls):
        return database.Column(database.String(255), nullable=False, server_default='')


class UniqueNamedModelMixin(NamedMixin):
    @declared_attr
    def name(cls):
        return database.Column(database.String(255), nullable=False, unique=True, server_default='')


class DatedModelMixin():
    @declared_attr
    def date_created(cls):
        return database.Column(database.DateTime(), default=datetime.now())


class DescriptionModelMixin(DescribedMixin):
    @declared_attr
    def description(cls):
        return database.Column(database.Text(), nullable=False, server_default=u'')


class ModelWithAssignedRoles:
    def has_role(self, person, name_of_role):
        def yes(assignment):
            return assignment.person == person and assignment.role.is_named(name_of_role)

        return any(map(yes, self.assignments))

class RootDescendantMixin:
    @property
    def ancestor(self):
        if self.is_top:
            return self.root
        else:
            return self.parent_object
    @property
    def url_on_delete(self):
        return self.ancestor.url



class NamedBaseModel(IdModelMixin, NamedModelMixin, DescriptionModelMixin, HierarchicalMixin, DatedModelMixin,
                     database.Model):
    __abstract__ = True


class UniqueNamedBaseModel(IdModelMixin, UniqueNamedModelMixin, DescriptionModelMixin, HierarchicalMixin,
                           DatedModelMixin, database.Model):
    __abstract__ = True
