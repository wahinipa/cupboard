#  Copyright (c) 2022, Wahinipa LLC
from flask import Blueprint, redirect
from flask_login import current_user, login_required

from tracking import database
from tracking.admin.administration import redirect_hacks
from tracking.forms.choice_forms import ChoiceUpdateForm
from tracking.modelling.choice_models import find_choice_by_id
from tracking.routing.home_redirect import home_redirect

# from tracking.commons.cupboard_display_context import display_context

choice_bp = Blueprint(
    'choice_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@choice_bp.route('/delete/<int:choice_id>')
@login_required
def choice_delete(choice_id):
    choice = find_choice_by_id(choice_id)
    if choice is not None and choice.user_may_delete(current_user):
        category = choice.category
        database.session.delete(choice)
        database.session.commit()
        return redirect(category.url)
    else:
        return redirect_hacks()


@choice_bp.route('/view/<int:choice_id>')
@login_required
def choice_view(choice_id):
    choice = find_choice_by_id(choice_id)
    if choice is not None and choice.may_be_observed(current_user):
        return choice.display_context(current_user).render_template()
    else:
        return home_redirect()


# @choice_bp.route('/update/<int:choice_id>', methods=['GET', 'POST'])
# @login_required
# def choice_update(choice_id):
#     choice = find_choice_by_id(choice_id)
#     if choice and choice.user_may_update(current_user):
#         form = choice_update_form(choice)
#         if request.method == 'POST' and form.cancel_button.data:
#             return redirect(url_for('choice_bp.choice_view', choice_id=choice_id))
#         if form.validate_on_submit():
#             update_choice_from_form(choice, form)
#             database.session.commit()
#             return redirect(url_for('choice_bp.choice_view', choice_id=choice.id))
#         else:
#             return render_template('pages/form_page.j2', form=form, tab="choice", **display_context())
#     else:
#         return redirect_hacks()


def choice_update_form(choice):
    return ChoiceUpdateForm(obj=choice)


def update_choice_from_form(choice, form):
    form.populate_obj(choice)
