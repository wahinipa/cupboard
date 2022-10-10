# Copyright (c) 2022, Wahinipa LLC

from flask_wtf import FlaskForm
from wtforms import SubmitField

from tracking.commons.base_forms import cancel_button_field, description_form_field, name_form_field
from tracking.things.old_thing_models import find_or_create_thing


class ThingBaseForm(FlaskForm):
    name = name_form_field()
    description = description_form_field()
    cancel_button = cancel_button_field()


class ThingCreateForm(ThingBaseForm):
    submit = SubmitField('Create New Thing')


class ThingUpdateForm(ThingBaseForm):
    submit = SubmitField('Update Thing')


def create_thing_from_form(parent_thing, form):
    return find_or_create_thing(form.name.data, form.description.data, kind_of=parent_thing)
