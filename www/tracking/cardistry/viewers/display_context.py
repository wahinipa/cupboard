#  Copyright (c) 2022, Wahinipa LLC
from flask import render_template

from tracking.contextual.context import Context


class DisplayContext(Context):
    def __init__(self, context=None, **kwargs):
        super().__init__()
        if context is not None:
            self.add_context(context)
        if kwargs:
            self.add_context(kwargs)

    def add_bread_crumbs(self, bread_crumbs):
        self['bread_crumb_list'] = bread_crumbs

    def add_child_context(self, child_context):
        self.append_to_list('children', child_context)

    def add_multiline_notation(self, label=None, tag=None, url=None, multiline=None):
        if multiline:
            lines = multiline.split("\n")
            if len(lines) > 1:
                self.add_notation(label=label, tag=tag, url=url, lines=lines)
            else:
                self.add_notation(label=label, tag=tag, url=url, value=multiline)

    def add_notation(self, label=None, tag=None, url=None, value=None, lines=None):
        notation = {
        }
        if label:
            notation['label'] = label
        if tag:
            notation['tag'] = tag
        if url:
            notation['url'] = url
        if value:
            notation['value'] = value
        if lines:
            notation['lines'] = lines
        self.append_notation(notation)

    def append_notation(self, notation):
        self.append_to_list('notations', notation)

    def render_template(self, template=None, **kwarg):
        if template is None:
            template = self["page_template"]
        return render_template(template, **kwarg, **self.as_dictionary)
