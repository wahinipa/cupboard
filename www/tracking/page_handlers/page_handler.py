#  Copyright (c) 2022, Wahinipa LLC
from tracking.routing.home_redirect import home_redirect


class PageHandler:

    def handle(self):
        return self.render() or home_redirect()

    def render(self):
        return self.objects_are_valid and self.viewer_has_permission and self.validated_rendering()
