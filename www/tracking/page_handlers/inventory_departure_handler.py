#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.inventory_forms import create_departure_form, remove_quantity_from_form
from tracking.page_handlers.inventory_base_handler import InventoryBaseHandler


class InventoryDepartureHandler(InventoryBaseHandler):

    def create_form(self):
        return create_departure_form(self.platter)

    @property
    def form_title(self):
        return f'Remove departing {self.description} from {self.platter.place.name}'

    def submit_action(self):
        return remove_quantity_from_form(self.platter, self.form)
