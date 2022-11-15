#  Copyright (c) 2022, Wahinipa LLC
from tracking.forms.inventory_forms import create_transfer_form, move_quantity_from_form
from tracking.modelling.role_models import Role
from tracking.page_handlers.inventory_base_handler import InventoryBaseHandler


class InventoryTransferHandler(InventoryBaseHandler):
    required_role_name = Role.transfer_role_name

    def viewer_has_special_permissions(self, viewer):
        return viewer and self.destination and self.destination.viewer_has_role(viewer, Role.inbound_role_name)

    def create_form(self):
        return create_transfer_form(self.platter)

    @property
    def form_title(self):
        return f'Transfer {self.description} from {self.place.name} to {self.destination.name}'

    def submit_action(self):
        return move_quantity_from_form(self.platter, self.form)
