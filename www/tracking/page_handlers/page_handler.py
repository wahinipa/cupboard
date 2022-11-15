#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role
from tracking.routing.home_redirect import home_redirect


class PageHandler:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def handle(self):
        return self.render() or home_redirect()

    def render(self):
        return self.action_is_allowed() and self.validated_rendering()

    def action_is_allowed(self):
        return self.objects_are_valid and \
               self.viewer_has_permission() and \
               self.viewer_has_special_permissions()

    def viewer_has_permission(self):
        return self.platter.viewer_has_endpoint_role(self.endpoint)

    def viewer_has_special_permissions(self):
        return self.viewer is not None
