#  Copyright (c) 2022, Wahinipa LLC


class DisplayContext:
    def __init__(self, context=None, title=None, project_name=None):
        if context is None:
            context = {}
        self.context = context
        if title is not None:
            self.add_attribute('title', title)
        if project_name is not None:
            self.add_attribute('project_name', project_name)

    def add_attribute(self, key, value):
        self.context[key] = value

    def add_action(self, url, label, task):
        self.context.setdefault('actions', []).append({
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

    @property
    def display_context(self):
        return self.context
