#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.cardistry_models import bread_crumbs
from tracking.viewers.all_roles import AllRoles
from tracking.viewers.role_viewing_base import RoleViewingBase


class RoleViewer(RoleViewingBase):

    def viewable_children(self, viewer):
        return self.base_children(viewer)

    @property
    def name(self):
        return self.role.name

    @property
    def label(self):
        return self.role.label

    def add_description(self, context):
        self.role.add_description(context)

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [AllRoles(person=self.person, place=self.place), self], target=self)
