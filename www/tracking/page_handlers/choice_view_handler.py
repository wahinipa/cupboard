#  Copyright (c) 2022, Wahinipa LLC


from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.page_handlers.choice_base_handler import ChoiceBaseHandler
from tracking.page_handlers.view_handler import ViewHandler


class ChoiceViewHandler(ChoiceBaseHandler, ViewHandler):
    page_template = 'pages/choice_view.j2'

    @property
    def display_context_maker(self):
        return self.thing_specification

    @property
    def display_attributes(self):
        return {
            'description': True,
            'children': [self.choice, self.thing, self.thing_specification],
            'children_attributes': dual_view_childrens_attributes(thing=self.thing),
        }
