#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for

from tracking.commons.old_base_models import TrackableMixin
from tracking.commons.cupboard_display_context import CupboardDisplayContext
from tracking.commons.text_utilities import description_notation_list


class PseudoModel(TrackableMixin):
    def __init__(self,
                 label,
                 endpoint,
                 description,
                 parent_object,
                 classification="All",
                 ):
        self.name = label  # TrackableMixin generates label from name.
        self.endpoint = endpoint
        self._parent_object = parent_object
        self.description = description
        self._classification = classification

    @property
    def child_list(self):
        return []

    @property
    def classification(self):
        return self._classification

    @property
    def parent_object(self):
        return self._parent_object

    @property
    def url(self):
        return url_for(self.endpoint)

    @property
    def parent_list(self):
        if self.parent_object is None:
            return []
        else:
            return [self.parent_object]

    def viewable_children(self, viewer):
        return [child for child in self.child_list if child.may_be_observed(viewer)]

    def viewable_attributes(self, viewer):
        attributes = {
            'classification': self.classification,
            'name': self.name,
            'label': self.label,
            'view_url': self.url,
            'notations': description_notation_list(description=self.description)
        }
        return attributes

    def display_context(self, viewer):
        context = CupboardDisplayContext({
            'label': self.label,
            'target': self.viewable_attributes(viewer),
            'children': [child.viewable_attributes(viewer) for child in self.viewable_children(viewer)],
            'parent_list': self.parent_list,
        })
        self.add_actions(context, viewer)
        return context

    def add_actions(self, context, viewer):
        pass
