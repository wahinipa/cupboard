#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.inventory_model import Inventory


def register_inventory_navigation(navigator):
    def register(task):
        endpoint = f'inventory_bp.inventory_{task}'
        navigator.register(Inventory, task, endpoint)

    register('arriving')
    register('departing')
    register('moving')
