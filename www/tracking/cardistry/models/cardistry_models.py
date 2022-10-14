#  Copyright (c) 2022, Wahinipa LLC


def name_is_key(record):
    return record.name


def sorted_by_name(listing):
    return sorted(listing, key=name_is_key)


class NamedMixin:
    @property
    def label(self):
        return self.name


class DescribedMixin:
    def add_description(self, display_context):
        display_context.add_multiline_notation(label="Description", multiline=self.description)


class HierarchicalMixin:

    @property
    def is_top(self):
        return self.parent_object is None

    @property
    def root_path(self):
        parent = self.parent_object
        path = parent.root_path if parent else []
        path.append(self)
        return path

    @property
    def top(self):
        top = self
        parent = self.parent_object
        while parent:
            top = parent
            parent = parent.parent_object
        return top

    def bread_crumbs(self, navigator):
        return bread_crumbs(navigator, self.root_path, target=self)

    @property
    def sorted_children(self):
        return sorted_by_name(self.children)


def bread_crumbs(navigator, path, target=None):
    def bread_crumb(item):
        crumb = {'label': item.label}
        url = navigator.url(item, 'view')
        if url and item != target:
            crumb['url'] = url
        return crumb

    return [bread_crumb(item) for item in path]
