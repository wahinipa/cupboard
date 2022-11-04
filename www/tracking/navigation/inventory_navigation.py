#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.inventory_viewer import InventoryViewer


def register_inventory_navigation(navigator):
    def register(task):
        endpoint = f'inventory_bp.inventory_{task}'
        navigator.register(InventoryViewer, task, endpoint)

    register('arriving')
    register('departing')
    register('moving')
