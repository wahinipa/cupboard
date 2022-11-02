#  Copyright (c) 2022, Wahinipa LLC
from flask import request, redirect

from tracking.contexts.cupboard_display_context import CupboardDisplayContext


class FormHandler:

    def __init__(self):
        self.navigator = None
        self.form = None

    def extra_render_template_args(self):
        return {}

    def validated_rendering(self):
        self.navigator = self.create_navigator()
        self.form = self.create_form()
        if request.method == 'POST' and self.form.cancel_button.data:
            return redirect(self.cancel_redirect_url)
        elif self.form.validate_on_submit():
            target = self.submit_action()
            return target and redirect(self.success_redirect_url(target))
        else:
            return self.render_template()

    def render_template(self):
        return self.display_context.render_template(self.page_template, form=self.form, form_title=self.form_title,
                                                    **self.extra_render_template_args())

    @property
    def display_context(self):
        return CupboardDisplayContext()
