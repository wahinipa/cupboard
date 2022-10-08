#  Copyright (c) 2022, Wahinipa LLC


def name_is_key(record):
    return record.name


class NamedMixin:
    @property
    def label(self):
        return self.name


class DescribedMixin:
    def add_description(self, display_context):
        display_context.add_multiline_notation(label="Description", multiline=self.description)


class HierarchicalMixin:

    @property
    def root_path(self):
        parent = self.parent_object
        path = parent.root_path if parent else []
        path.append(self)
        return path

    @property
    def bread_crumbs(self):
        return bread_crumbs(self.root_path, target=self)


def bread_crumbs(path, target=None):
    def bread_crumb(item):
        crumb = {'label': item.label}
        url = item.url
        if url and item != target:
            crumb['url'] = url
        return crumb

    return [bread_crumb(item) for item in path]
