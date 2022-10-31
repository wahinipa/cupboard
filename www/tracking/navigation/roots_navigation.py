#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.roots_model import Roots


def register_roots_navigation(navigator):
    def register(task):
        endpoint = f'roots_bp.roots_{task}'
        navigator.register(Roots, task, endpoint)

    register('view')
    register('create')
