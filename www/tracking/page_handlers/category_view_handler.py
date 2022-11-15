#  Copyright (c) 2022, Wahinipa LLC


from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.modelling.role_models import Role
from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.page_handlers.view_handler import ViewHandler
from tracking.viewers.model_viewer import ModelViewer


class CategoryViewHandler(CategoryBaseHandler, ViewHandler):
    page_template = 'pages/category_view.j2'
    required_role_name = Role.admin_role_name

    @property
    def display_context_maker(self):
        return ModelViewer(self.root)

    @property
    def display_attributes(self):
        return {
            'description': True,
            'children': [self.category, self.thing, self.thing_specification],
            'children_attributes': dual_view_childrens_attributes(thing=self.thing),
        }
