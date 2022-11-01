#  Copyright (c) 2022, Wahinipa LLC

class PageHandler:

    def render(self):
        return self.objects_are_valid and self.viewer_has_permission and self.validated_rendering()
