#  Copyright (c) 2022, Wahinipa LLC
from flask_wtf import FlaskForm
from wtforms import SubmitField


class RoleBaseForm(FlaskForm):
    pass


class RoleCreateForm(RoleBaseForm):
    submit = SubmitField('Create Role')


class RoleUpdateForm(RoleBaseForm):
    submit = SubmitField('Update Role')
