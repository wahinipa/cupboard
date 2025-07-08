#  Copyright (c) 2022, Wahinipa LLC
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import BooleanField, HiddenField, PasswordField, StringField, SubmitField, validators
from wtforms.validators import DataRequired

from tracking import database
from tracking.forms.cardistry_forms import about_me_form_field, cancel_button_field
from tracking.modelling.people_model import find_or_create_user, find_person_by_username


class LoginForm(FlaskForm):
    next = HiddenField()  # for login.j2
    reg_next = HiddenField()  # for login_or_register.html

    username = StringField('Username', validators=[
        DataRequired('Username is required'),
    ])
    password = PasswordField('Password', validators=[
        DataRequired('Password is required'),
    ])
    remember_me = BooleanField('Remember me')

    submit = SubmitField('Sign in')

    def found_user(self):
        return find_person_by_username(self.username.data)

    def validate(self, extra_validators=None):
        # Validate field-validators
        if super(LoginForm, self).validate(extra_validators):
            # Find user
            user = self.found_user()
            if user:
                if check_password_hash(user.password, self.password.data):
                    return True
                else:
                    self.password.errors.append('Incorrect Password')
            else:
                self.username.errors.append(f'{self.username} does not exist')
        return False


class UserProfileForm(FlaskForm):
    """
    Form class for modifying user profile.
    """
    first_name = StringField('First Name', [DataRequired('First Name is required')])
    last_name = StringField('Last Name', [DataRequired('Last Name is required')])
    about_me = about_me_form_field()
    cancel_button = cancel_button_field()
    submit = SubmitField('Save')


class UserCreateForm(FlaskForm):
    """
    Form class for creating a new user.
    """
    username = StringField('Username', [DataRequired('Username is required')])
    first_name = StringField('First Name', [DataRequired('First Name is required')])
    last_name = StringField('Last Name', [DataRequired('Last Name is required')])
    is_admin = BooleanField('Is Admin')
    password_new = PasswordField(label='New Password', validators=[
        validators.Length(min=6, max=10),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField(label='Confirm New Password', validators=[
        validators.Length(min=6, max=10)
    ])
    cancel_button = cancel_button_field()
    submit = SubmitField('Create New User')


class ChangePasswordForm(FlaskForm):
    """
    Form class for changing password.
    """
    password_old = PasswordField(label='Current Password', validators=[
        validators.Length(min=6, max=10)
    ])
    password_new = PasswordField(label='New Password', validators=[
        validators.Length(min=6, max=10),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField(label='Confirm New Password', validators=[
        validators.Length(min=6, max=10)
    ])
    cancel_button = cancel_button_field()
    submit = SubmitField('Save')

    def validate(self, extra_validators=None):
        # Validate field-validators
        if super(ChangePasswordForm, self).validate(extra_validators):
            if check_password_hash(current_user.password, self.password_old.data):
                password_new_hash = generate_password_hash(self.password_new.data)
                if check_password_hash(password_new_hash, self.password_confirm.data):
                    return True
                else:
                    self.password_new.errors.append('Password not confirmed')
            else:
                self.password_old.errors.append('Incorrect Password')
        return False


def create_user_from_form(form):
    username = form.username.data
    user = find_person_by_username(username)
    if user is None:
        find_or_create_user(
            form.first_name.data,
            form.last_name.data,
            username,
            form.password_new.data,
            form.is_admin.data
        )
        database.session.commit()
    return user
