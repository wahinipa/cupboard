#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.people_base_handler import PeopleBaseHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.viewers.model_viewer import ModelViewer


class PeopleViewHandler(PeopleBaseHandler, ViewHandler):
    page_template = 'pages/person_view.j2'

    @property
    def display_context_maker(self):
        return ModelViewer(self.person)

    @property
    def objects_are_valid(self):
        return self.person and True

    @property
    def display_attributes(self):
        return {
            'add_tasks': True,
            'description': True,
            'url': True,
            'bread_crumbs': True,
        }
