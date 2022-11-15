#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.inventory_forms import create_adjustment_form, adjust_quantity_on_form
from tracking.modelling.role_models import Role
from tracking.page_handlers.inventory_base_handler import InventoryBaseHandler


class InventoryAdjustmentHandler(InventoryBaseHandler):
    required_role_name = Role.adjust_role_name

    def create_form(self):
        return create_adjustment_form(self.platter)

    @property
    def form_title(self):
        return f'Adjust {self.description} at {self.place.name}'

    def submit_action(self):
        adjust_quantity_on_form(self.platter, self.form)
        return self.root
