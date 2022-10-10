#  Copyright (c) 2022, Wahinipa LLC
from os import environ

from tracking.cardistry.viewers.display_context import DisplayContext


def project_name():
    return environ.get('PROJECT_NAME', 'Wahinipa Cupboard Tracker')


def project_title():
    return environ.get('WEBSITE_TITLE', 'Wahinipa')


class CupboardDisplayContext(DisplayContext):
    def __init__(self, context=None, page_template=None):
        if page_template is None:
            page_template = "pages/card_content.j2"
        super().__init__(
            context=context,
            page_template=page_template,
            title=project_title(),
            project_name=project_name(),
        )


class CupboardDisplayContextMixin:
    def display_context(self, viewer, as_child=True):
        context = CupboardDisplayContext(context={
            'label': self.name,
            'classification': self.classification,
        }, page_template=self.page_template)
        self.add_description(context)
        if as_child:
            context.add_attribute('url', self.url)
        else:
            context.add_bread_crumbs(self.bread_crumbs)
            for child in self.viewable_children(viewer):
                context.add_child_display_context(child.display_context(viewer))
        return context
