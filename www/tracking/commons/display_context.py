#  Copyright (c) 2022, Wahinipa LLC
from os import environ


def project_name():
    return display_context()['project_name']


def display_context(context=None):
    return DisplayContext(context).display_context


class DisplayContext:
    def __init__(self, context=None):
        if context is None:
            context = {}
        self.context = context
        self.context.setdefault('title', environ.get('WEBSITE_TITLE', 'Wahinipa'))
        self.context.setdefault('project_name', environ.get('PROJECT_NAME', 'Wahinipa Cupboard Tracker'))

    def add_attribute(self, key, value):
        self.context[key] = value

    def add_action(self, url, label, task):
        self.context.setdefault('actions', []).append({
            'url': url,
            'label': label,
            'task': task,
        })

    @property
    def display_context(self):
        return self.context
