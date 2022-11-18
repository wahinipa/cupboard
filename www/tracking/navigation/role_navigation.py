#  Copyright (c) 2022, Wahinipa LLC
#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role


def register_role_navigation(navigator):
    navigator.register(Role, 'view', 'role_bp.role_view', [Role.anybody_role_name])
