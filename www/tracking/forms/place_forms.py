#  Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from wtforms import SubmitField

from tracking import database
from tracking.cardistry.forms.cardistry_forms import NameDescriptionBaseForm
from tracking.modelling.place_model import Place


def create_place_from_form(form):
    place = Place(
        name=form.name.data,
        description=form.description.data,
        date_created=datetime.now()
    )
    database.session.add(place)
    database.session.commit()
    return place


class PlaceCreateForm(NameDescriptionBaseForm):
    submit = SubmitField('Create New Place')


class PlaceUpdateForm(NameDescriptionBaseForm):
    submit = SubmitField('Update Place')

