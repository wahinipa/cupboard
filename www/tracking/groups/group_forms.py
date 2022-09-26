# Copyright (c) 2022, Wahinipa LLC
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField

from tracking import database
from tracking.commons.base_forms import cancel_button_field, description_form_field, name_form_field
from tracking.groups.group_models import Group


class GroupBaseForm(FlaskForm):
    name = name_form_field()
    description = description_form_field()
    cancel_button = cancel_button_field()


class GroupCreateForm(GroupBaseForm):
    submit = SubmitField('Create New Group')

class GroupUpdateForm(GroupBaseForm):
    submit = SubmitField('Update Group')


def create_group_from_form(form):
    group = Group(
        name=form.name.data,
        description=form.description.data,
        date_created=datetime.now()
    )
    database.session.add(group)
    database.session.commit()
    return group
