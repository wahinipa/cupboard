#  Copyright (c) 2022, Wahinipa LLC
#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import AllRoles, Role


def register_role_navigation(navigator):
    navigator.register(AllRoles, 'view', 'role_bp.role_list', [Role.anybody_role_name])
    navigator.register(Role, 'view', 'role_bp.role_view', [Role.anybody_role_name])
