#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for

from tracking.commons.base_models import TrackableMixin
from tracking.commons.display_context import DisplayContext


class PseudoModel(TrackableMixin):
    def __init__(self,
                 label,
                 endpoint,
                 description,
                 parent_object,
                 child_list=None,
                 classification="All",
                 ):
        if child_list is None:
            child_list = []
        self._child_list = child_list
        self.name = label  # TrackableMixin generates label from name.
        self.endpoint = endpoint
        self._parent_object = parent_object
        self.description = description
        self._classification = classification

    def viewable_child_list(self, viewer):
        return self._child_list

    @property
    def classification(self):
        return self._classification

    @property
    def parent_object(self):
        return self._parent_object

    @property
    def one_line_description(self):
        return self.description

    @property
    def description_lines(self):
        if self.description:
            return [self.description]
        else:
            return []

    @property
    def url(self):
        return url_for(self.endpoint)

    @property
    def parent_list(self):
        if self.parent_object is None:
            return []
        else:
            return self.parent_object.parent_list

    def viewable_attributes(self, viewer):
        attributes = {
            'classification': self.classification,
            'name': self.name,
            'label': self.label,
            'view_url': self.url,
            'lines': self.description_lines,
            'children': [child.viewable_attributes(viewer) for child in self.viewable_child_list(viewer)]
        }
        return attributes

    def display_context(self, viewer):
        context = DisplayContext({
            'target': self.viewable_attributes(viewer),
            'name': self.name,
            'label': self.label,
            'parent_list': self.parent_list,
        })
        return context.display_context


class HomeModel(PseudoModel):
    def __init__(self):
        super().__init__(
            label='Home',
            endpoint='home_bp.home',
            description="Start Here",
            parent_object=None,
            classification="Root"
        )
        self.all_categories = PseudoModel(
            label="Categories",
            endpoint='category_bp.category_list',
            description="Categories are lists of Choices for being more specific about Things",
            parent_object=self,
        )
        self.all_groups = PseudoModel(
            label="Groups",
            endpoint='group_bp.group_list',
            description="Groups have Places which have Things",
            parent_object=self
        )
        self.all_places = PseudoModel(
            label="Places",
            endpoint='place_bp.place_list',
            description="Places are locations where Groups keep Things",
            parent_object=self
        )
        self.all_people = PseudoModel(
            label="People",
            endpoint='people_bp.people_list',
            description="User Accounts",
            parent_object=self
        )
        self.all_things = PseudoModel(
            label="Things",
            endpoint='thing_bp.thing_list',
            description="Things are inventory items that needs tracking",
            parent_object=self
        )
        self._child_list = [
            self.all_groups,
            self.all_places,
            self.all_people,
            self.all_things,
            self.all_categories,
        ]


home_root = HomeModel()


