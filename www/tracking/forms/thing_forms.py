#  Copyright (c) 2022, Wahinipa LLC

from wtforms import SubmitField

from tracking.cardistry.forms.cardistry_forms import NameDescriptionBaseForm


class ThingCreateForm(NameDescriptionBaseForm):
    submit = SubmitField('Create New Thing')


class ThingUpdateForm(NameDescriptionBaseForm):
    submit = SubmitField('Update Thing')
