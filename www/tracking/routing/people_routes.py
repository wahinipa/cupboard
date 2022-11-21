#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, flash, redirect, request, url_for
from flask_admin.helpers import is_safe_url
from flask_login import current_user, login_required, login_user, logout_user

from tracking import database
from tracking.commons.redirect_hackers import redirect_hackers
from tracking.contexts.cupboard_display_context import CupboardDisplayContext
from tracking.forms.people_forms import ChangePasswordForm, LoginForm
from tracking.page_handlers.people_create_handler import PeopleCreateHandler
from tracking.page_handlers.people_delete_handler import PeopleDeleteHandler
from tracking.page_handlers.people_disable_handler import PeopleDisableHandler
from tracking.page_handlers.people_enable_handler import PeopleEnableHandler
from tracking.page_handlers.people_list_handler import PeopleListHandler
from tracking.page_handlers.people_update_handler import PeopleUpdateHandler
from tracking.page_handlers.people_view_handler import PeopleViewHandler
from tracking.routing.home_redirect import home_redirect

people_bp = Blueprint(
    'people_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@people_bp.route('/create', methods=['GET', 'POST'])
@login_required
def people_create():
    return PeopleCreateHandler('people_bp.people_create', current_user).handle()


@people_bp.route('/delete/<int:person_id>')
@login_required
def people_delete(person_id):
    return PeopleDeleteHandler('people_bp.people_delete', current_user, person_id=person_id).handle()

@people_bp.route('/enable/<int:person_id>')
@login_required
def people_enable(person_id):
    return PeopleEnableHandler('people_bp.people_enable', current_user, person_id=person_id).handle()

@people_bp.route('/disable/<int:person_id>')
@login_required
def people_disable(person_id):
    return PeopleDisableHandler('people_bp.people_disable', current_user, person_id=person_id).handle()


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
        return CupboardDisplayContext(None).render_template('pages/login.j2', form=form)


@people_bp.route('/update/<int:person_id>', methods=['GET', 'POST'])
@login_required
def people_update(person_id):
    return PeopleUpdateHandler('people_bp.people_update', current_user, person_id=person_id).handle()


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
    return CupboardDisplayContext(current_user).render_template('pages/change_password.j2', form=form)


@people_bp.route('/list')
@login_required
def people_list():
    return PeopleListHandler('people_bp.people_list', current_user).handle()


@people_bp.route('/view/<int:person_id>')
@login_required
def people_view(person_id):
    return PeopleViewHandler('people_bp.people_view', current_user, person_id=person_id).handle()
