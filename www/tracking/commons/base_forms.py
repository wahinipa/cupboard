#  Copyright (c) 2022, Wahinipa LLC
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired


def name_form_field():
    return StringField('Name', validators=[
        DataRequired('Name is required'),
    ])


def description_form_field(description=None):
    if description is None:
        description = 'Use to track additional details.'
    return TextAreaField('Description', description=description)


def details_form_field(description=None):
    if description is None:
        description = 'Use to track additional details.'
    return TextAreaField('Details', description=description)


def cancel_button_field(label='Cancel'):
    return SubmitField(label=label, render_kw={'formnovalidate': True})
