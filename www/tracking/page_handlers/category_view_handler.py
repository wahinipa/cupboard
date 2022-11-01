#  Copyright (c) 2022, Wahinipa LLC


from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.page_handlers.view_handler import ViewHandler


class CategoryViewHandler(CategoryBaseHandler, ViewHandler):
    page_template = 'pages/category_view.j2'

    @property
    def display_context_maker(self):
        return self.root

    @property
    def display_attributes(self):
        return {
            'description': True,
            'children': [self.category, self.thing, self.thing_specification],
            'children_attributes': dual_view_childrens_attributes(thing=self.thing),
        }