#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role
from tracking.viewers.thing_specification_viewer import ThingSpecificationViewer


def register_inventory_navigation(navigator):
    def register(task, role_names):
        endpoint = f'inventory_bp.inventory_{task}'
        navigator.register(ThingSpecificationViewer, task, endpoint, role_names)

    register('arriving', [Role.inbound_role_name, Role.super_role_name])
    register('departing', [Role.outbound_role_name, Role.super_role_name])
    register('moving', [Role.transfer_role_name, Role.super_role_name])
    register('changing', [Role.adjust_role_name, Role.super_role_name])
