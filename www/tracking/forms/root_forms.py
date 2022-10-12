#  Copyright (c) 2022, Wahinipa LLC

from wtforms import SubmitField

from tracking.cardistry.forms.cardistry_forms import NameDescriptionBaseForm
from tracking.modelling.root_model import create_root


def create_root_from_form(form):
    return create_root(
        name=form.name.data,
        description=form.description.data
    )


class RootCreateForm(NameDescriptionBaseForm):
    submit = SubmitField('Create New Root')


class RootUpdateForm(NameDescriptionBaseForm):
    submit = SubmitField('Update Root')
