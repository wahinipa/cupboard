#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.cardistry_models import bread_crumbs
from tracking.modelling.role_models import Role
from tracking.viewers.all_roles import AllRoles
from tracking.viewers.role_viewing_base import RoleViewingBase


class RoleViewer(RoleViewingBase):

    def viewable_children(self, viewer):
        return self.base_children(viewer)

    @property
    def name(self):
        return self.role.name

    @property
    def identities(self):
        role_id = self.role.id if self.role else 0
        person_id = self.person.id if self.person else 0
        place_id = self.place.id if self.place else 0
        return {
            'role_id': role_id,
            'person_id': person_id,
            'place_id': place_id,
        }

    @property
    def label(self):
        if self.person and self.role:
            if self.place:
                if self.role.name in Role.root_role_name_set:
                    return f'{self.person.name} as {self.role.label} for {self.place.root.label}'
                elif self.role.name in Role.place_role_name_set:
                    return f'{self.person.name} as {self.role.label} at {self.place.label}'
            return f'{self.person.name} as {self.role.label}'
        else:
            return self.role.label

    @property
    def possible_tasks(self):
        tasks = self.possible_role_tasks
        if self.place and self.place.root and self.person:
            if self.person.is_linked(self.place.root):
                tasks += ['unlink']
            else:
                tasks += ['link']
        return tasks

    @property
    def possible_role_tasks(self):
        if self.role and self.person:
            role_name = self.role.name
            if role_name in Role.universal_role_name_set:
                if self.person.has_universal_role(role_name):
                    return ['deny']
                else:
                    return ['grant']
            elif self.place:
                if self.person.has_exact_role(role_name, place=self.place):
                    return ['deny']
                else:
                    return ['grant']
        return []

    def add_description(self, context):
        self.role.add_description(context)

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, [AllRoles(person=self.person, place=self.place), self], target=self)
