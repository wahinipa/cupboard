#  Copyright (c) 2022, Wahinipa LLC
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


def name_form_field():
    """
    Create form field for a name.
    :return:
    """
    return StringField('Name', validators=[
        DataRequired('Name is required'),
    ])


def description_form_field(description=None):
    """
    Create form field for a description.
    :param description:
    :return:
    """
    if description is None:
        description = 'Use to track additional details.'
    return TextAreaField('Description', description=description)


def about_me_form_field(description=None):
    """
    Create an "about me" form field.
    :param description:
    :return:
    """
    if description is None:
        description = 'More about the person.'
    return TextAreaField('About Me', description=description)


def cancel_button_field(label='Cancel'):
    """
    Create a cancel button form field.
    :param label:
    :return:
    """
    return SubmitField(label=label, render_kw={'formnovalidate': True})


class NameDescriptionBaseForm(FlaskForm):
    """
    Base form that includes name, description, and cancel button.
    """
    name = name_form_field()
    description = description_form_field()
    cancel_button = cancel_button_field()
