#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.cardistry_models import bread_crumbs
from tracking.modelling.role_models import all_roles
from tracking.viewers.role_viewing_base import RoleViewingBase


class AllRoles(RoleViewingBase):

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

    def add_description(self, context):
        pass

    def viewable_children(self, viewer):
        return self.base_children(viewer) + all_roles()

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [self], target=self)

    def may_perform_task(self, viewer, task):
        return False
