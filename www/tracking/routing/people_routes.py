#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_admin.helpers import is_safe_url
from flask_login import current_user, login_required, login_user, logout_user

from tracking import database
from tracking.commons.redirect_hackers import redirect_hackers
from tracking.forms.people_forms import ChangePasswordForm, LoginForm, UserCreateForm, UserProfileForm, \
    create_user_from_form
from tracking.modelling.people_model import find_user_by_id, all_people_display_context, AllPeople
from tracking.modelling.people_view_handler import PeopleViewHandler
from tracking.navigation.cupboard_navigation import create_cupboard_navigator
from tracking.navigation.dual_navigator import DualNavigator
from tracking.page_handlers.people_create_handler import PeopleCreateHandler
from tracking.page_handlers.people_delete_handler import PeopleDeleteHandler
from tracking.page_handlers.people_update_handler import PeopleUpdateHandler
from tracking.routing.home_redirect import home_redirect
from tracking.contexts.cupboard_display_context import CupboardDisplayContext

people_bp = Blueprint(
    'people_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@people_bp.route('/create', methods=['GET', 'POST'])
@login_required
def people_create():
    handler = PeopleCreateHandler(current_user)
    return handler.render() or home_redirect()


@people_bp.route('/delete/<int:user_id>')
@login_required
def people_delete(user_id):
    handler = PeopleDeleteHandler(current_user, user_id=user_id)
    return handler.render() or home_redirect()


@people_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.found_user()
        login_user(user)

        flash('Logged in successfully.')

        next_url = request.args.get('next')
        if next_url:
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if is_safe_url(next_url):
                return redirect(next_url)
            else:
                return redirect_hackers()
        else:
            return home_redirect()
    else:
        return CupboardDisplayContext().render_template('pages/login.j2', form=form)


@people_bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
@login_required
def people_update(user_id):
    handler = PeopleUpdateHandler(current_user, user_id=user_id)
    return handler.render() or home_redirect()


@people_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('people_bp.login'))


@people_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'POST' and form.cancel_button.data:
        return home_redirect()
    if form.validate_on_submit():
        database.session.commit()
        return home_redirect()
    return CupboardDisplayContext().render_template('pages/change_password.j2', form=form)


@people_bp.route('/list')
@login_required
def people_list():
    navigator = create_cupboard_navigator()
    return all_people_display_context(navigator, current_user).render_template(
        "pages/people_list.j2", active_flavor="people")


@people_bp.route('/view/<int:user_id>')
@login_required
def people_view(user_id):
    handler = PeopleViewHandler(current_user, user_id=user_id)
    return handler.render() or home_redirect()
