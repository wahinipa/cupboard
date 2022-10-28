#  Copyright (c) 2022, Wahinipa LLC

from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField

from tracking.forms.cardistry_forms import cancel_button_field
from tracking.modelling.cardistry_models import sorted_by_name


class SpecificationBaseForm(FlaskForm):
    pass


def unique_class_name_from_choices(category, choices, has_unknown):
    new_class_name = f'Specification_Custom_Form_{category.id}'
    if has_unknown:
        new_class_name += '_u'
    for choice in choices:
        new_class_name += f'_{choice.id}'
    return new_class_name


def field_name_for_choice(choice):
    return f'choose_{choice.id}'


def create_dynamic_specification_form(category, currently_selected_choices, has_unknown):
    # Dynamically create a unique class derived from SpecificationBaseForm
    form_class_name = unique_class_name_from_choices(category, currently_selected_choices, has_unknown)
    new_class = type(form_class_name, (SpecificationBaseForm,), {})

    def add_checkmark(name, label, description, current_value):
        if current_value:
            default = 'checked'
        else:
            default = None
        setattr(new_class, name, BooleanField(label, validators=[], description=description, default=default))

    current_has_any = not currently_selected_choices
    any_label = "Any"
    any_description = f'Include all items, regardless of choice of {category.name}'
    add_checkmark('choose_any', any_label, any_description, current_has_any)

    unknown_label = f'Unknown {category.name}'
    unknown_description = f'Include items where choice of {category.name} is not known.'
    add_checkmark('choose_unknown', unknown_label, unknown_description, has_unknown)

    # Add checkbox fields to the class, one per choice
    sorted_category_choices = sorted_by_name(category.choices)
    for choice in sorted_category_choices:
        field_name = field_name_for_choice(choice)
        label = choice.name
        description = f'Include {choice.name} {category.name}.'
        current_value = choice in currently_selected_choices
        add_checkmark(name=field_name, label=label, description=description, current_value=current_value)

    # Create and add cancel & submit button last, so it sorts to the end of the form when displayed.
    setattr(new_class, 'cancel_button', cancel_button_field())
    submit = SubmitField(f'Update {category.name} Search Options')
    setattr(new_class, 'submit', submit)
    form = new_class()
    return form


def update_specification_form(category, specification):
    currently_selected_choices = specification.choices_for(category)
    has_unknown = category in specification.unknowns
    return create_dynamic_specification_form(category, currently_selected_choices, has_unknown)


def update_specification(category, specification, form):
    any_is_selected = form.choose_any.data
    if any_is_selected:
        selected_choices = set()  # empty set is interpreted as accepting any choice including unknown
        has_unknown = False
    else:
        def choice_is_selected(choice):
            field_name = field_name_for_choice(choice)
            return getattr(form, field_name).data

        selected_choices = {choice for choice in category.choices if choice_is_selected(choice)}
        has_unknown = form.choose_unknown.data

    specification_choices_for_other_categories = {choice for choice in specification.choices
                                                  if choice.category != category}
    new_specification_choices = specification_choices_for_other_categories | selected_choices

    this_category_set = {category}
    current_unknowns = specification.unknowns
    if has_unknown:
        new_unknowns = current_unknowns | this_category_set
    else:
        new_unknowns = current_unknowns - this_category_set

    return category.root.find_or_create_specification(new_specification_choices, new_unknowns)
