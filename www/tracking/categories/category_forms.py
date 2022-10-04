#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField

from tracking import database
from tracking.categories.category_models import Category
from tracking.commons.base_forms import name_form_field, description_form_field, cancel_button_field


class CategoryBaseForm(FlaskForm):
    name = name_form_field()
    description = description_form_field()
    cancel_button = cancel_button_field()


class CategoryCreateForm(CategoryBaseForm):
    submit = SubmitField('Create New Category')

class CategoryUpdateForm(CategoryBaseForm):
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