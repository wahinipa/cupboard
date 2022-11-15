#  Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking import database


class TargetDeleteHandler:
    def validated_rendering(self):
        # Calculate the redirect url...
        redirect_url = self.delete_redirect_url
        # ...before deleting anything that might be used to calculate the redirect url
        database.session.delete(self.target)
        database.session.commit()
        return redirect(redirect_url)

