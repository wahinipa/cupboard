#  Copyright (c) 2022, Wahinipa LLC
from os import environ

from tracking.viewing.display_context import DisplayContext


def project_name():
    return environ.get('PROJECT_NAME', 'Wahinipa Cupboard Tracker')


def project_title():
    return environ.get('WEBSITE_TITLE', 'Wahinipa')


class CupboardDisplayContext(DisplayContext):
    def __init__(self, context=None, **kwargs):
        super().__init__(
            context=context,
            title=project_title(),
            project_name=project_name(),
            **kwargs
        )


class CupboardDisplayContextMixin:
    def add_task(self, context, navigator, task):
        context.add_task(url=navigator.url(self, task), label=self.task_label(task), task=task)

    def task_label(self, task):
        prefix = self.label_prefixes.get(task, '')
        return f'{prefix}{self.name}'

    def display_context(self, navigator, viewer, display_attributes):
        children_attributes = display_attributes.get('children_attributes')
        if children_attributes:
            children = display_attributes.get('children', self.viewable_children(viewer))
        else:
            children = []
        context = CupboardDisplayContext(context={
            'label': self.name,
            'classification': self.singular_label,
            'flavor': self.flavor,
        })
        if display_attributes.get('description'):
            self.add_description(context)
        if display_attributes.get('url'):
            context['url'] = navigator.url(self, 'view')
        if display_attributes.get('bread_crumbs'):
            context.add_bread_crumbs(self.bread_crumbs(navigator))
        for child in children:
            child_attributes = children_attributes.get(child.flavor)
            if child_attributes:
                child_display_context_attributes = child_attributes.get('display_context')
                if child_display_context_attributes is not None:
                    context.add_child_context(child.display_context(navigator, viewer,child_display_context_attributes))
                if child_attributes.get('notation'):
                    child_link_label = child.singular_label
                    context.add_notation(label=child_link_label, url=navigator.url(child, 'view'), value=child.name)
        for task in self.allowed_tasks(viewer):
            self.add_task(context, navigator, task)
        return context

    def allowed_tasks(self, viewer):
        return [task for task in self.possible_tasks if self.may_perform_task(viewer, task)]