#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role
from tracking.modelling.root_model import Root


def register_root_navigation(navigator):
    def register(task, role_names):
        endpoint = f'root_bp.root_{task}'
        navigator.register(Root, task, endpoint, role_names)

    register('delete', [Role.super_role_name])
    register('view', [Role.roots_observer_role_name, Role.linkage_role_name, Role.super_role_name])
    register('update', [Role.super_role_name])
