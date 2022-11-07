#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.people_model import User, AllPeople
from tracking.viewers.people_list_viewer import PeopleListViewer


def register_people_navigation(navigator):

    def register(task):
        endpoint = f'people_bp.people_{task}'
        navigator.register(User, task, endpoint)

    register('create')
    register('delete')
    register('list')
    register('update')
    register('view')

    navigator.register(AllPeople, 'view', 'people_bp.people_list')
    navigator.register(PeopleListViewer, 'create', 'people_bp.people_create')
