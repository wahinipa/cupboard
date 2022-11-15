#  Copyright (c) 2022, Wahinipa LLC
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.cardistry_models import bread_crumbs
from tracking.modelling.people_model import all_people


class PeopleListViewer(CupboardDisplayContextMixin):
    singular_label = "People"
    plural_label = "People"
    possible_tasks = ['create']
    label_prefixes = {}
    flavor = "people"
    label = "People"

    @property
    def identities(self):
        return {}

    @property
    def name(self):
        return "User Account"

    @property
    def parent_object(self):
        return None

    @property
    def root_path(self):
        return [self]

    def viewable_children(self, viewer):
        # TODO: refine this test
        return all_people()

    def add_description(self, context):
        pass

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [self], target=self)

    def may_perform_task(self, viewer, task):
        if task == 'create':
            return viewer.may_create_person
        else:
            return False
