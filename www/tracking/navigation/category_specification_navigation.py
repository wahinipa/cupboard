#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role
from tracking.viewers.category_specification_viewer import CategorySpecificationViewer

def register_category_specification_navigation(navigator):
    endpoint = f'specification_bp.specification_update'
    # Actually does an update, but url generation defaults to 'view'
    navigator.register(CategorySpecificationViewer, 'view', endpoint, [Role.observer_role_name, Role.super_role_name])
