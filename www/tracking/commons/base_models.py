#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from sqlalchemy.orm import declared_attr

from tracking import database


class IdModelMixin():
    @declared_attr
    def id(cls):
        return database.Column(database.Integer, primary_key=True)

    @property
    def unique_id(self):
        return f'{self.__class__.__name__}_{self.id}'


class KnowsOwnName:
    def is_named(self, name):
        return self.name == name


class NamedModelMixin(KnowsOwnName):
    @declared_attr
    def name(cls):
        return database.Column(database.String(255), nullable=False, server_default='')


class UniqueNamedModelMixin(KnowsOwnName):
    @declared_attr
    def name(cls):
        return database.Column(database.String(255), nullable=False, unique=True, server_default='')


class DatedModelMixin():
    @declared_attr
    def date_created(cls):
        return database.Column(database.DateTime(), default=datetime.now())


class DescriptionModelMixin():
    @declared_attr
    def description(cls):
        return database.Column(database.Text(), nullable=False, server_default=u'')

    @property
    def description_lines(self):
        return self.description.split('\n')


class ModelWithRoles:
    def has_role(self, person, name_of_role):
        def yes(assignment):
            return assignment.person == person and assignment.role.is_named(name_of_role)

        return any(map(yes, self.assignments))


class BaseModel(IdModelMixin, NamedModelMixin, DescriptionModelMixin, DatedModelMixin, database.Model):
    __abstract__ = True


class UniqueNamedBaseModel(IdModelMixin, UniqueNamedModelMixin, DescriptionModelMixin, DatedModelMixin, database.Model):
    __abstract__ = True
