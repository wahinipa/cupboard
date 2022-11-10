#  Copyright (c) 2022, Wahinipa LLC
from os import environ

from tracking.contexts.display_context import DisplayContext


def project_name():
    return environ.get('PROJECT_NAME', 'Wahinipa Cupboard Tracker')


def project_title():
    return environ.get('WEBSITE_TITLE', 'Wahinipa')


class CupboardDisplayContext(DisplayContext):
    def __init__(self, viewer, context=None, **kwargs):
        super().__init__(
            context=context,
            title=project_title(),
            project_name=project_name(),
            **kwargs
        )
        self.viewer = viewer

    def add_top_menu_item(self, label, url, flavor, activity=None):
        self.append_to_list('top_menu_items', {
            'label': label,
            'url': url,
            'flavor': flavor,
            'activity': activity or flavor,
        })

    def set_active_flavor(self, current_activity):
        self['current_activity'] = current_activity


class CupboardDisplayContextMixin:
    def add_task(self, context, navigator, task, label=None):
        if label is None:
            label = self.task_label(task)
        is_required = task.endswith('ing')
        context.add_task(url=navigator.url(self, task), label=label, task=task, is_required=is_required)

    def task_label(self, task):
        prefix = self.label_prefixes.get(task, '')
        return f'{prefix}{self.name}'

    def prefix(self):
        return f'{self.singular_label}: '

    def display_context(self, navigator, viewer, display_attributes, source_inventory, destination_inventory):
        prefix = display_attributes.get('prefix', self.prefix())
        children_attributes = display_attributes.get('children_attributes')
        if children_attributes:
            children = display_attributes.get('children', self.viewable_children(viewer))
        else:
            children = []
        context = CupboardDisplayContext(viewer, context={
            'label': self.name,
            'prefix': prefix,
            'flavor': self.flavor,
        })

        if display_attributes.get('source_quantity'):
            self.add_quantity(context, source_inventory)
        if display_attributes.get('destination_quantity'):
            self.add_quantity(context, destination_inventory)
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
                    context.add_child_context(
                        child.display_context(navigator, viewer, child_display_context_attributes, source_inventory, destination_inventory))
                if child_attributes.get('notation'):
                    child_link_label = child.singular_label
                    if child_attributes.get('source_quantity'):
                        inventory = source_inventory.place_inventory(child)
                    elif child_attributes.get('destination_quantity'):
                        inventory = destination_inventory.place_inventory(child)
                    else:
                        inventory = None
                    if inventory:
                        quantity = inventory.quantity
                        value = f'{child.name} has {quantity}'
                    else:
                        value = child.name
                    context.add_notation(label=child_link_label, url=navigator.url(child, 'view'), value=value)
        for task in self.allowed_tasks(viewer):
            self.add_task(context, navigator, task)
        extra_action_parameters = display_attributes.get('extra_action_parameters')
        if extra_action_parameters:
            self.add_extra_actions(context, navigator, viewer, **extra_action_parameters)
        return context

    def allowed_tasks(self, viewer):
        return [task for task in self.possible_tasks if self.may_perform_task(viewer, task)]

    def add_quantity(self, context, inventory):
        quantity = inventory.quantity
        context.add_notation(label='Quantity', value=f'{quantity}')
