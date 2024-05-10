#  Copyright (c) 2022, Wahinipa LLC

class Context:
    """
    Dictionary mimic with added methods to help with display contexts.
    """

    def __init__(self):
        self.context = {}

    def __setitem__(self, key, value):
        self.context.__setitem__(key, value)

    def __getitem__(self, key):
        return self.context.__getitem__(key)

    def __ior__(self, other):
        self.add_context(other)
        return self

    def add_context(self, context):
        """
        Merge another context or dictionary into self content.
        Works easily with **kwargs dictionaries.

        :param context:
        :return:
        """
        for key, value in context.items():
            self[key] = value

    def append_to_list(self, list_key, value):
        """
        Add value to list, creating new list if needed.

        :param list_key: Dictionary key
        :param value: Value to add to list
        :return:
        """
        if value:
            self.context.setdefault(list_key, []).append(value)

    @property
    def as_dictionary(self):
        """
        Replace Context objects with dictionaries that templates can understand.
        :return: dictionary equivalent to self.
        """
        return Context.filter(self.context)

    @staticmethod
    def filter(value):
        """
        Recursively clean replacing Context with dictionaries.

        :param value:
        :return:
        """
        if hasattr(value, 'as_dictionary'):
            return value.as_dictionary
        elif isinstance(value, list):
            return [Context.filter(item) for item in value]
        elif isinstance(value, dict):
            return {key: Context.filter(item) for key, item in value.items()}
        else:
            return value

    def get(self, key, default=None):
        return self.context.get(key, default)

    def items(self):
        return self.context.items()

    def setdefault(self, key, default=None):
        return self.context.setdefault(key, default)
