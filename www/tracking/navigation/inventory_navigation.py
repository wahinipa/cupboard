#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.thing_specification_viewer import ThingSpecificationViewer


def register_inventory_navigation(navigator):
    def register(task):
        endpoint = f'inventory_bp.inventory_{task}'
        navigator.register(ThingSpecificationViewer, task, endpoint)

    register('arriving')
    register('departing')
    register('moving')
    register('changing')
