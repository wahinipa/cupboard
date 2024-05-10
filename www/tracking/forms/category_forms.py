#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField

from tracking import database
from tracking.forms.cardistry_forms import cancel_button_field, description_form_field, name_form_field
from tracking.modelling.category_model import Category


class CategoryBaseForm(FlaskForm):
    name = name_form_field()
    description = description_form_field()
    cancel_button = cancel_button_field()


class CategoryCreateForm(CategoryBaseForm):
    """
    Form class for creating a category.
    """
    submit = SubmitField('Create New Category')


class CategoryUpdateForm(CategoryBaseForm):
    """
    Form class for updating a category.
    """
    submit = SubmitField('Update Category')


def create_category_from_form(form):
    category = Category(
        name=form.name.data,
        description=form.description.data,
        date_created=datetime.now()
    )
    database.session.add(category)
    database.session.commit()
    return category


def update_category_from_form(category, form):
    form.populate_obj(category)
    return category
