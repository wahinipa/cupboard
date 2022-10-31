#  Copyright (c) 2022, Wahinipa LLC

class PageHandler:

    def __init__(self, viewer):
        self.viewer = viewer

    def render(self):
        if self.objects_are_valid and self.viewer_has_permission:
            return self.validated_rendering()
        else:
            return None

