# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField

from tracking import database
from tracking.commons.base_forms import cancel_button_field, description_form_field, name_form_field
from tracking.places.place_models import Place


class PlaceBaseForm(FlaskForm):
    name = name_form_field()
    description = description_form_field()
    cancel_button = cancel_button_field()


class PlaceCreateForm(PlaceBaseForm):
    submit = SubmitField('Create New Place')


class PlaceUpdateForm(PlaceBaseForm):
    submit = SubmitField('Update Place')


def create_place_from_form(group, form):
    place = Place(
        group_id = group.id,
        name=form.name.data,
        description=form.description.data,
        date_created=datetime.now()
    )
    database.session.add(place)
    database.session.commit()
    return place
