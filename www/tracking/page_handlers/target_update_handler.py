#  Copyright (c) 2022, Wahinipa LLC

class TargetUpdateHandler:
    @property
    def cancel_redirect_url(self):
        return self.redirect_url

    @property
    def form_title(self):
        return f'Update {self.target.name}'

    @property
    def redirect_url(self):
        return self.navigator.url(self.target, 'view')

    def success_redirect_url(self, target):
        return self.redirect_url

    @property
    def viewer_has_permission(self):
        return self.target.may_update(self.viewer)
