#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from sqlalchemy.orm import declared_attr

from tracking import database
from tracking.modelling.cardistry_models import DescribedMixin, HierarchicalMixin, NamedMixin


class Descriptor:
    """
    Wrapper utility holds flavor, label, and name.
    """

    def __init__(self, flavor, label, name):
        self.flavor = flavor
        self.singular_label = label
        self.name = name


class IdModelMixin():
    """
    Mixin class for models. Holds standard id but also has unique_id property that includes class.
    """

    @declared_attr
    def id(cls):
        """
        Database table id.
        :return:
        """
        return database.Column(database.Integer, primary_key=True)

    @property
    def unique_id(self):
        """
        Return identifier that is unique across models of differing class.
        id is only unique for items of same class (i.e. database table id).
        :return:
        """
        return f'{self.__class__.__name__}_{self.id}'


class NamedModelMixin(NamedMixin):
    """
    Mixin class for models with a name column. Name need not be unique.
    """

    @declared_attr
    def name(cls):
        return database.Column(database.String(255), nullable=False, server_default='')


class UniqueNamedModelMixin(NamedMixin):
    """
    Mixin class for models with a name column. Name MUST be unique.
    """

    @declared_attr
    def name(cls):
        return database.Column(database.String(255), nullable=False, unique=True, server_default='')


class DatedModelMixin():
    """
    Mixin class for models with a creation date column.
    """

    @declared_attr
    def date_created(cls):
        return database.Column(database.DateTime(), default=datetime.now())


class DescriptionModelMixin(DescribedMixin):
    """
    Mixin class for models with a description column.
    """

    @declared_attr
    def description(cls):
        return database.Column(database.Text(), nullable=False, server_default=u'')


class RootDescendantMixin:
    """
    Mixin class for models that might have a parent object.
    """

    @property
    def ancestor(self):
        if self.is_top:
            return self.root
        else:
            return self.parent_object


class NamedBaseModel(IdModelMixin, NamedModelMixin, DescriptionModelMixin, HierarchicalMixin, DatedModelMixin,
                     database.Model):
    """
    Base model for classes with id, name, description, creation date, and parentage
    """
    __abstract__ = True  # Used as base class, not an actual database table.

    def __repr__(self):
        return f'{self.__class__.__name__}-{self.name}-{self.id}'


class UniqueNamedBaseModel(IdModelMixin, UniqueNamedModelMixin, DescriptionModelMixin, HierarchicalMixin,
                           DatedModelMixin, database.Model):
    """
    Mixin class for models with a ZZZ column.
    """
    __abstract__ = True  # Used as base class, not an actual database table.
