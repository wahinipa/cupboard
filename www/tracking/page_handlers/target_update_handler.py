#  Copyright (c) 2022, Wahinipa LLC

class TargetUpdateHandler:
    @property
    def cancel_redirect_url(self):
        return self.target_update_redirect()

    @property
    def form_title(self):
        return f'Update {self.target.name}'

    def success_redirect_url(self, target):
        return self.target_update_redirect()

    def target_update_redirect(self):
        return self.navigator.url(self.target, 'view')

    @property
    def viewer_has_permission(self):
        return self.target.may_update(self.viewer)
