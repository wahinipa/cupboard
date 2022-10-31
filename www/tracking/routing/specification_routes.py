#  Copyright (c) 2022, Wahinipa LLC

from flask import Blueprint, request, redirect
from flask_login import login_required, current_user

from tracking.forms.specification_forms import update_specification, \
    create_specification_form_descriptor, create_dynamic_specification_form
from tracking.modelling.category_model import find_category_by_id
from tracking.viewers.platter import create_platter, Platter
from tracking.routing.home_redirect import home_redirect
from tracking.contexts.cupboard_display_context import CupboardDisplayContext

specification_bp = Blueprint(
    'specification_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@specification_bp.route('/update/<int:category_id>/<int:place_id>/<int:thing_id>/<int:specification_id>',
                        methods=['GET', 'POST'])
@login_required
def specification_update(category_id, place_id, thing_id, specification_id):
    platter = create_platter(place_id=place_id, thing_id=thing_id, specification_id=specification_id)
    category = find_category_by_id(category_id)
    if category and platter.may_be_observed(current_user) and platter.root == category.root \
        and platter.specification.may_update(current_user):
        specification = platter.specification
        form_descriptor = create_specification_form_descriptor(category, specification)
        form = create_dynamic_specification_form(form_descriptor)
        if request.method == 'POST' and form.cancel_button.data:
            navigator = platter.create_navigator()
            redirect_url = navigator.url(platter.root, 'view')
            return redirect(redirect_url)
        elif form.validate_on_submit():
            new_specification = update_specification(category, specification, form)
            new_platter = Platter(root=platter.root, place=platter.place, thing=platter.thing,
                                    specification=new_specification)
            navigator = new_platter.create_navigator()
            redirect_url = navigator.url(platter.root, 'view')
            return redirect(redirect_url)
        else:
            return CupboardDisplayContext().render_template(
                'pages/specification_update.j2', form_descriptor=form_descriptor, form=form,
                form_title=f'Update {specification.name}')
    else:
        return home_redirect()
