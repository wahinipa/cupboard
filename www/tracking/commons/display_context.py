#  Copyright (c) 2022, Wahinipa LLC
from os import environ


def display_context(context=None):
    if context is None:
        context = {}
    context.setdefault('title', environ.get('WEBSITE_TITLE', 'Wahinipa'))
    context.setdefault('project_name', environ.get('PROJECT_NAME', 'Wahinipa Cupboard Tracker'))
    return context
