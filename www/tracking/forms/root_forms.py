#  Copyright (c) 2022, Wahinipa LLC

from wtforms import SubmitField

from tracking.forms.cardistry_forms import NameDescriptionBaseForm
from tracking.modelling.root_model import create_root


class RootCreateForm(NameDescriptionBaseForm):
    """
    Form class for root creation.
    """
    submit = SubmitField('Create New Root')


class RootUpdateForm(NameDescriptionBaseForm):
    """
    Form class for root update.
    """
    submit = SubmitField('Update Root')


def update_root_from_form(root, form):
    form.populate_obj(root)


def create_root_from_form(form):
    return create_root(
        name=form.name.data,
        description=form.description.data
    )
