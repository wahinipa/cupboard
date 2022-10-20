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

    def display_context(self, navigator, viewer, as_child=True, child_depth=0, children=None):
        if children is None:
            children = self.viewable_children(viewer)
        context = CupboardDisplayContext(context={
            'label': self.name,
            'classification': self.singular_label,
        })
        self.add_description(context)
        if as_child:
            context['url'] = navigator.url(self, 'view')
        if child_depth > 0:
            context.add_bread_crumbs(self.bread_crumbs(navigator))
            for child in children:
                if child_depth > 1:
                    context.add_child_context(child.display_context(navigator, viewer, child_depth=child_depth - 1))
                else:
                    child_link_label = child.singular_label
                    context.add_notation(label=child_link_label, url=navigator.url(child, 'view'), value=child.name)
        for task in self.allowed_tasks(viewer):
            self.add_task(context, navigator, task)
        context['flavor'] = self.flavor
        return context

    def allowed_tasks(self, viewer):
        return [task for task in self.possible_tasks if self.may_perform_task(viewer, task)]
