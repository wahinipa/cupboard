#  Copyright (c) 2022, Wahinipa LLC

from wtforms import SubmitField

from tracking.forms.cardistry_forms import NameDescriptionBaseForm


class ThingCreateForm(NameDescriptionBaseForm):
    """ Flask form for creating a Thing object """
    submit = SubmitField('Create New Thing')


class ThingUpdateForm(NameDescriptionBaseForm):
    """ Flask form for updating a Thing object """
    submit = SubmitField('Update Thing')


def update_thing_from_form(thing, form):
    """
    Transfer form content to a thing.

    :param thing: target thing object
    :param form: filled out form returned by submit action.
    :return:
    """
    form.populate_obj(thing)
