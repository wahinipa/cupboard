#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField

from tracking import database
from tracking.choices.choice_models import Choice
from tracking.commons.base_forms import name_form_field, description_form_field, cancel_button_field


class ChoiceBaseForm(FlaskForm):
    name = name_form_field()
    description = description_form_field()
    cancel_button = cancel_button_field()


class ChoiceCreateForm(ChoiceBaseForm):
    submit = SubmitField('Create New Choice')

class ChoiceUpdateForm(ChoiceBaseForm):
    submit = SubmitField('Update Choice')


def create_choice_from_form(category, form):
    choice = Choice(
        category_id=category.id,
        name=form.name.data,
        description=form.description.data,
        date_created=datetime.now()
    )
    database.session.add(choice)
    database.session.commit()
    return choice
