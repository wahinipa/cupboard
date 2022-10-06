#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_admin.helpers import is_safe_url
from flask_login import current_user, login_required, login_user, logout_user

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.commons.display_context import display_context
from tracking.home.home_models import home_root
from tracking.people.people_forms import ChangePasswordForm, LoginForm, UserCreateForm, UserProfileForm
from tracking.people.people_models import find_or_create_user, find_user_by_id, find_user_by_username

people_bp = Blueprint(
    'people_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@people_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.may_create_person:
        form = UserCreateForm()
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('people_bp.people_list'))
        if form.validate_on_submit():
            user = create_user_from_form(form)
            if user:
                return redirect(user.url)
            else:
                return redirect(url_for('people_bp.people_list'))
        return render_template('form_page.j2', form=form, form_title=f'Create New User Account', **display_context())
    else:
        return redirect_hacks()


def create_user_from_form(form):
    username = form.username.data
    user = find_user_by_username(username)
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


@people_bp.route('/delete/<int:user_id>')
@login_required
def people_delete(user_id):
    person = find_user_by_id(user_id)
    if person and current_user.may_delete_person(person):
        database.session.delete(person)
        database.session.commit()
        return redirect(url_for('people_bp.people_list'))
    else:
        return redirect_hacks()


@people_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.found_user()
        login_user(user)

        flash('Logged in successfully.')

        next_url = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if next_url and not is_safe_url(next_url):
            return abort(400)

        return redirect(next_url or url_for('home_bp.home'))
    else:
        return render_template('login.j2', form=form, **display_context())


@people_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfileForm(obj=current_user)
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('home_bp.home'))
    if form.validate_on_submit():
        form.populate_obj(current_user)
        database.session.commit()
        return redirect(url_for('home_bp.home'))

    return render_template('form_page.j2', form=form, form_title=f'Update Profile for {current_user.name}',
                           **display_context())


@people_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('people_bp.login'))


@people_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('home_bp.home'))
    if form.validate_on_submit():
        database.session.commit()
        return redirect(url_for('home_bp.home'))
    return render_template('change_password.j2', form=form, **display_context())


@people_bp.route('/list')
@login_required
def people_list():
    return home_root.all_people.display_context(current_user).render_template()


@people_bp.route('/view/<int:user_id>')
@login_required
def people_view(user_id):
    person = find_user_by_id(user_id)
    if person and current_user.may_view_person(person):
        return person.display_context(current_user).render_template()
    else:
        return redirect(url_for('home_bp.home'))
