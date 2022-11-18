#  Copyright (c) 2022, Wahinipa LLC
from tracking.contexts.cupboard_display_context import CupboardDisplayContextMixin
from tracking.viewers.people_list_viewer import PeopleListViewer


class RoleViewingBase(CupboardDisplayContextMixin):
    page_template = 'pages/role_view.j2'
    singular_label = "Roles"
    plural_label = "Roles"
    possible_tasks = []
    label_prefixes = {}
    flavor = "role"
    label = "Roles"

    def __init__(self, place, person, role=None):
        self.place = place
        self.person = person
        self.role = role

    def base_children(self, viewer):
        children = []
        if self.person:
            children.append(self.person)
        else:
            children.append(PeopleListViewer())
        if self.place:
            children.append(self.place)
        return children

    @property
    def display_attributes(self):
        return {
            'add_tasks': True,
            'description': True,
            'url': True,
            'bread_crumbs': True,
            'children_attributes': {
                'role': {
                    'notation': True,
                },
                'place': {
                    'display_context': {
                        'add_tasks': True,
                        'description': True,
                        'url': True,
                        'bread_crumbs': True,
                        'prefix': None,
                        'children_attributes': {
                            'place': {
                                'notation': True,
                            },
                        },
                    },
                },
                'people': {
                    'display_context': {
                        'add_tasks': True,
                        'description': True,
                        'url': True,
                        'bread_crumbs': True,
                        'prefix': None,
                        'children_attributes': {
                            'people': {
                                'notation': True,
                            },
                        },
                    },
                }
            },
        }
