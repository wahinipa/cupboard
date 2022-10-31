#  Copyright (c) 2022, Wahinipa LLC

from tracking.forms.inventory_forms import create_arrival_form, add_quantity_from_form
from tracking.page_handlers.inventory_base_handler import InventoryBaseHandler


class InventoryArrivalHandler(InventoryBaseHandler):

    def create_form(self):
        return create_arrival_form(self.platter)

    @property
    def form_title(self):
        return f'Add arriving {self.description} at {self.place.name}'

    def submit_action(self):
        return add_quantity_from_form(self.platter, self.form)
