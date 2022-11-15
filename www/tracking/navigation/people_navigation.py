#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.people_model import User, AllPeople
from tracking.modelling.role_models import Role
from tracking.viewers.people_list_viewer import PeopleListViewer


def register_people_navigation(navigator):
    def register(task, role_names):
        endpoint = f'people_bp.people_{task}'
        navigator.register(User, task, endpoint, role_names)

    register('create', [Role.super_role_name])
    register('delete', [Role.super_role_name])
    register('disable', [Role.super_role_name])
    register('enable', [Role.super_role_name])
    register('list', [Role.people_viewer_name, Role.linkage_role_name, Role.super_role_name])
    register('update', [Role.super_role_name])
    register('view', [Role.self_role_name, Role.linkage_role_name, Role.people_viewer_name, Role.super_role_name])

    navigator.register(AllPeople, 'view', 'people_bp.people_list',
                       [Role.people_viewer_name, Role.linkage_role_name, Role.super_role_name])
    navigator.register(PeopleListViewer, 'create', 'people_bp.people_create', [Role.super_role_name])
