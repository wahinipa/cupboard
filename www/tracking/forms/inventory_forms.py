#  Copyright (c) 2022, Wahinipa LLC
from flask_wtf import FlaskForm
from wtforms import IntegerField, validators, SubmitField

from tracking.forms.cardistry_forms import cancel_button_field
from tracking.modelling.postioning_model import add_quantity_of_things, change_quantity_of_things, \
    move_quantity_of_things


class InventoryArrivalForm(FlaskForm):
    quantity = IntegerField(label="Quantity Arriving", default=1, validators=[
        validators.DataRequired(),
        validators.NumberRange(min=1)
    ])
    cancel_button = cancel_button_field()
    submit = SubmitField('Add Arrival')


def create_arrival_form(platter):
    return InventoryArrivalForm()


def add_quantity_from_form(platter, form):
    quantity = form.quantity.data
    if quantity > 0:
        return add_quantity_of_things(platter.place, platter.thing, platter.specification, quantity)
    else:
        return 0


def remove_quantity_from_form(platter, form):
    quantity = form.quantity.data
    if quantity > 0:
        return add_quantity_of_things(platter.place, platter.thing, platter.specification, -quantity)


def create_departure_form(platter):
    max_value = platter.current_quantity
    class_name = f'InventoryDepartingForm_{max_value}'
    new_class = type(class_name, (FlaskForm,), {})
    quantity_field = IntegerField(label="Quantity Departing", default=1, validators=[
        validators.DataRequired(),
        validators.NumberRange(min=1, max=max_value)
    ])
    setattr(new_class, 'quantity', quantity_field)
    setattr(new_class, 'cancel_button', cancel_button_field())
    setattr(new_class, 'submit', SubmitField('Remove Departing Items from Inventory'))
    form = new_class()
    return form


class InventoryAdjustmentForm(FlaskForm):
    quantity = IntegerField(label="Quantity Arriving", default=1, validators=[
        validators.DataRequired(),
        validators.NumberRange(min=0)
    ])
    cancel_button = cancel_button_field()
    submit = SubmitField('Add Arrival')


def create_adjustment_form(platter):
    return InventoryAdjustmentForm()


def adjust_quantity_on_form(platter, form):
    requested_quantity = form.quantity.data
    return change_quantity_of_things(platter.place, platter.thing, platter.specification, requested_quantity)


def create_transfer_form(platter):
    max_value = platter.current_quantity
    class_name = f'InventoryTransferForm{max_value}'
    new_class = type(class_name, (FlaskForm,), {})
    quantity_field = IntegerField(label="Quantity to Transfer", default=1, validators=[
        validators.DataRequired(),
        validators.NumberRange(min=1, max=max_value)
    ])
    setattr(new_class, 'quantity', quantity_field)
    setattr(new_class, 'cancel_button', cancel_button_field())
    setattr(new_class, 'submit', SubmitField(f'Transfer from {platter.place.name} to {platter.destination.name}'))
    form = new_class()
    return form


def move_quantity_from_form(platter, form):
    transfer_quantity = form.quantity.data
    return move_quantity_of_things(platter.destination, platter.place, platter.thing, platter.specification, transfer_quantity)
