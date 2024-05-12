#  Copyright (c) 2022, Wahinipa LLC


def name_is_key(record):
    """
    Used as sorting key function to sort by name

    :param record:
    :return:
    """
    return record.name


def sorted_by_name(listing):
    """
    Returns a list sorted by name.

    :param listing: list to sort
    :return: sorted list
    """
    return sorted(listing, key=name_is_key)


class NamedMixin:
    """
    Mixin for classes that use name property as object label.
    label is used for creating breadcrumbs.
    """

    @property
    def label(self):
        return self.name


class DescribedMixin:
    """
    Mixin class knows how to add its description to a display context.
    """

    def add_description(self, display_context):
        display_context.add_multiline_notation(label="Description", multiline=self.description)


class HierarchicalMixin:
    """
    Mixin class adds navigational utilities for objects in a hierarchy or tree.
    Assumes class has properties parent_object and children.
    """

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
        """
        Returns list of children sorted by name.
        Fails if children do not have name property.
        :return:
        """
        return sorted_by_name(self.children)

    @property
    def direct_set(self):
        return {self}

    @property
    def full_set(self):
        """
        Generates set of self and full hierarchy below.
        Works for tree or directed graph with no loops.
        :return:
        """
        full_set = self.direct_set
        for child in self.children:
            full_set |= child.full_set
        return full_set


def bread_crumbs(navigator, path, target=None):
    """
    Creates a bread crumb list.
    Each item in the list has a label.
    All items except optional target have a url.

    :param navigator: Knows how to make urls for items.
    :param path: List of items.
    :param target: Optional item that should not get a url (i.e. current view)
    :return: bread crumb list
    """

    def bread_crumb(item):
        crumb = {'label': item.label}
        url = navigator.target_url(item, 'view')
        if url and item != target:
            crumb['url'] = url
        return crumb

    return [bread_crumb(item) for item in path]
