#  Copyright (c) 2022, Wahinipa LLC
from flask import render_template


class OldDisplayContext:
    def __init__(self, context=None, title=None, project_name=None, page_template=None):
        if context is None:
            context = {}
        self.context = context
        if title is not None:
            self.add_attribute('title', title)
        if project_name is not None:
            self.add_attribute('project_name', project_name)
        self.page_template = page_template

    def add_attribute(self, key, value):
        self.context[key] = value

    def add_bread_crumbs(self, bread_crumbs):
        self.add_attribute('bread_crumb_list', bread_crumbs)

    def add_task(self, url, label, task):
        self.context.setdefault('tasks', []).append({
            'url': url,
            'label': label,
            'task': task,
        })

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

    def append_to_list(self, list_key, value):
        if value:
            self.context.setdefault(list_key, []).append(value)

    def add_child_display_context(self, child_context):
        self.append_to_list('children', child_context.display_context)

    @property
    def display_context(self):
        return self.context

    def render_template(self, template=None, **kwarg):
        if template is None:
            template = self.page_template
        return render_template(template, **kwarg, **self.display_context)
