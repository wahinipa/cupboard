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
            page_template = page_template,
            title=project_title(),
            project_name=project_name(),
        )
