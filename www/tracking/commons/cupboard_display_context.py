#  Copyright (c) 2022, Wahinipa LLC
from os import environ

from cardistry.viewers.display_context import DisplayContext


def project_name():
    return environ.get('PROJECT_NAME', 'Wahinipa Cupboard Tracker')


def project_title():
    return environ.get('WEBSITE_TITLE', 'Wahinipa')


class CupboardDisplayContext(DisplayContext):
    def __init__(self, context=None):
        super().__init__(
            context=context,
            title=project_title(),
            project_name=project_name(),
        )
