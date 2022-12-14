#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.cardistry_models import bread_crumbs
from tracking.modelling.root_model import all_roots
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin


class RootsViewer(CupboardDisplayContextMixin):
    flavor = 'home'
    label = 'Associations'
    label_prefixes = {}
    singular_label = 'Home'
    possible_tasks = ['create']

    @property
    def identities(self):
        return {}

    @property
    def name(self):
        return self.label

    @property
    def parent_object(self):
        return None

    @property
    def root_path(self):
        return [self]

    def viewable_children(self, viewer):
        return [root for root in all_roots() if root.may_be_observed(viewer)]

    def add_description(self, context):
        pass

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [self], target=self)

    def may_perform_task(self, viewer, task):
        if task == 'create':
            return viewer.may_create_root
        else:
            return False
