#  Copyright (c) 2022, Wahinipa LLC
from os import environ

from tracking.cardistry.viewers.old_display_context import OldDisplayContext


def project_name():
    return environ.get('PROJECT_NAME', 'Wahinipa Cupboard Tracker')


def project_title():
    return environ.get('WEBSITE_TITLE', 'Wahinipa')


class CupboardDisplayContext(OldDisplayContext):
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
    @property
    def classification(self):
        return self.singular_label

    def display_context(self, viewer, as_child=True, child_link_label=None):
        context = CupboardDisplayContext(context={
            'label': self.name,
            'classification': self.classification,
        }, page_template=self.page_template)
        self.add_description(context)
        if as_child:
            context.add_attribute('url', self.url)
        else:
            context.add_bread_crumbs(self.bread_crumbs)
            self.add_additional_tasks(context, viewer)
            for child in self.viewable_children(viewer):
                if child_link_label:
                    context.add_notation(label=child_link_label, url=child.url, value=child.name)
                else:
                    context.add_child_display_context(child.display_context(viewer))
            if self.may_update(viewer):
                context.add_task(url=self.url_update, label=self.name, task="update")
            if self.may_delete(viewer):
                context.add_task(url=self.url_delete, label=self.name, task="delete")
        return context

    def add_additional_tasks(self, context, viewer):
        pass
