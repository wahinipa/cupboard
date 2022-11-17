#  Copyright (c) 2022, Wahinipa LLC
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin
from tracking.modelling.cardistry_models import bread_crumbs
from tracking.modelling.role_models import all_roles


class RoleListViewer(CupboardDisplayContextMixin):
    singular_label = "Role"
    plural_label = "Roles"
    possible_tasks = []
    label_prefixes = {}
    flavor = "role"
    label = "Role"

    @property
    def identities(self):
        return {}

    @property
    def name(self):
        return "Roles"

    @property
    def parent_object(self):
        return None

    @property
    def root_path(self):
        return [self]

    def viewable_children(self, viewer):
        # TODO: refine this test
        return all_roles()

    def add_description(self, context):
        pass

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [self], target=self)

    def may_perform_task(self, viewer, task):
        return False
