#  Copyright (c) 2022, Wahinipa LLC


class ModelViewer:

    def __init__(self, model):
        self.model = model

    def display_context(self, navigator, viewer, display_attributes):
        return self.model.display_context(navigator, viewer, display_attributes)

