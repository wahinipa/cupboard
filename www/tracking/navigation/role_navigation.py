#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.people_model import User
from tracking.modelling.role_models import Role
from tracking.viewers.role_viewer import RoleViewer


def register_role_navigation(navigator):
    navigator.register(Role, 'view', 'role_bp.role_view', [Role.anybody_role_name])
    navigator.register(RoleViewer, 'grant', 'role_bp.role_grant', [Role.control_role_name])
    navigator.register(RoleViewer, 'deny', 'role_bp.role_deny', [Role.control_role_name])
    navigator.register(RoleViewer, 'link', 'role_bp.role_link', [Role.user_admin_role_name, Role.super_role_name])
    navigator.register(RoleViewer, 'unlink', 'role_bp.role_unlink', [Role.user_admin_role_name, Role.super_role_name])
