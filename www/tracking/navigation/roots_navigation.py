#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role
from tracking.viewers.roots_viewer import RootsViewer


def register_roots_navigation(navigator):
    def register(task, role_names):
        endpoint = f'roots_bp.roots_{task}'
        navigator.register(RootsViewer, task, endpoint, role_names)

    register('view', [Role.roots_observer_role_name, Role.super_role_name])
    register('create', [Role.super_role_name])
