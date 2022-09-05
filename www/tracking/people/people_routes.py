#  Copyright (c) 2022. Wahinipa LLC
from flask import Blueprint, flash, request, abort, redirect, url_for, render_template
from flask_admin.helpers import is_safe_url
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.people.people_forms import UserCreateForm, LoginForm, UserProfileForm, ChangePasswordForm
from tracking.people.people_models import find_user_by_username, find_or_create_user

people_bp = Blueprint(
    'people_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@people_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_the_admin:
        form = UserCreateForm()
        if request.method == 'POST' and form.cancel_button.data:
            return redirect(url_for('home_bp.home'))
        if form.validate_on_submit():
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
            return redirect(url_for('home_bp.home'))
        return render_template('user_create.html', form=form)
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
    return render_template('login.html', form=form)


@people_bp.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = UserProfileForm(obj=current_user)
    if request.method == 'POST' and form.cancel_button.data:
        return redirect(url_for('home_bp.home'))
    if form.validate_on_submit():
        form.populate_obj(current_user)
        database.session.commit()
        return redirect(url_for('home_bp.home'))

    return render_template('profile.html', form=form)


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
        password_new_hash = generate_password_hash(form.password_new.data)
        current_user.password = password_new_hash
        database.session.commit()
        return redirect(url_for('home_bp.home'))
    return render_template('change_password.html', form=form)
