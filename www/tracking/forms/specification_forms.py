#  Copyright (c) 2022, Wahinipa LLC

from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField

from tracking.forms.cardistry_forms import cancel_button_field
from tracking.modelling.cardistry_models import sorted_by_name


class SpecificationBaseForm(FlaskForm):
    """
    Base class for creating Specification forms.
    Derived forms are created dynamically as they are different for each set of choices.
    """
    pass


def unique_class_name_from_choices(category, choices, has_unknown):
    """
    If the form looks different it must have a unique name.

    :param category:
    :param choices:
    :param has_unknown:
    :return:
    """
    new_class_name = f'Specification_Custom_Form_{category.id}'
    if has_unknown:
        new_class_name += '_u'
    for choice in choices:
        new_class_name += f'_{choice.id}'
    return new_class_name


def field_name_for_choice(choice):
    return f'choose_{choice.id}'


def create_specification_form_descriptor(category, specification):
    currently_selected_choices = specification.choices_for(category)
    has_unknown = category in specification.unknowns

    def describe_choice_box(choice):
        return {
            'field_name': field_name_for_choice(choice),
            'label': choice.name,
            'description': f'Include {choice.name} {category.name}.',
            'default': 'checked' if choice in currently_selected_choices else None,
        }

    sorted_category_choices = sorted_by_name(category.choices)

    return {
        'form_class_name': unique_class_name_from_choices(category, currently_selected_choices, has_unknown),
        'form_title': f'Update {specification.name}',
        'choices': [describe_choice_box(choice) for choice in sorted_category_choices],
        'unknown_field': {
            'field_name': 'choose_unknown',
            'label': f'Unknown {category.name}',
            'description': f'Include items where choice of {category.name} is not known.',
            'default': 'checked' if has_unknown else None,
        },
        'any_field': {
            'field_name': 'choose_any',
            'label': "Any",
            'description': f'Include all items, regardless of choice of {category.name}',
            'default': None,  # Always off since no user case for opening dialog and not making choices.
        },
        'submit_label': f'Update {category.name} Search Options',
    }


def create_dynamic_specification_form(form_descriptor):
    # Dynamically create a unique class derived from SpecificationBaseForm
    new_class = type(form_descriptor['form_class_name'], (SpecificationBaseForm,), {})

    def add_checkmark(box):
        setattr(new_class, box['field_name'],
                BooleanField(box['label'], validators=[], description=box['description'], default=box['default']))

    add_checkmark(form_descriptor['any_field'])
    add_checkmark(form_descriptor['unknown_field'])
    for box in form_descriptor['choices']:
        add_checkmark(box)

    # Create and add cancel & submit button last, so it sorts to the end of the form when displayed.
    setattr(new_class, 'cancel_button', cancel_button_field())
    setattr(new_class, 'submit', SubmitField(form_descriptor['submit_label']))
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
