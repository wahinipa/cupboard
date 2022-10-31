#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.categories_model import Categories


def register_categories_navigation(navigator):
    def register(task):
        endpoint = f'categories_bp.categories_{task}'
        navigator.register(Categories, task, endpoint)

    register('create')
    register('view')
