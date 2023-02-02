#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField

from tracking import database
from tracking.forms.cardistry_forms import name_form_field, description_form_field, cancel_button_field
from tracking.modelling.choice_model import Choice


class ChoiceBaseForm(FlaskForm):
    name = name_form_field()
    description = description_form_field()
    cancel_button = cancel_button_field()


class ChoiceCreateForm(ChoiceBaseForm):
    submit = SubmitField('Create New Choice')


class ChoiceUpdateForm(ChoiceBaseForm):
    submit = SubmitField('Update Choice')


def update_choice_from_form(choice, form):
    form.populate_obj(choice)
    return choice
