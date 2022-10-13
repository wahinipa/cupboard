#  Copyright (c) 2022, Wahinipa LLC

class Context:
    def __init__(self):
        self.context = {}

    def __setitem__(self, key, value):
        self.context.__setitem__(key, value)

    def __getitem__(self, key):
        return self.context.__getitem__(key)

    def get(self,key, default=None):
        return self.context.get(key, default)

    def setdefault(self, key, default=None):
        return self.context.setdefault(key, default)

    def items(self):
        return self.context.items()

    @staticmethod
    def filter(value):
        if hasattr(value, 'as_dictionary'):
            return value.as_dictionary
        elif isinstance(value, list):
            return [Context.filter(item) for item in value]
        elif isinstance(value, dict):
            return { key:Context.filter(item) for key, item in value.items()}
        else:
            return value

    @property
    def as_dictionary(self):
        return Context.filter(self.context)


