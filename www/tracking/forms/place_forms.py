#  Copyright (c) 2022, Wahinipa LLC

from wtforms import SubmitField

from tracking.forms.cardistry_forms import NameDescriptionBaseForm


class PlaceCreateForm(NameDescriptionBaseForm):
    submit = SubmitField('Create New Place')


class PlaceUpdateForm(NameDescriptionBaseForm):
    submit = SubmitField('Update Place')


def update_place_from_form(place, form):
    form.populate_obj(place)
