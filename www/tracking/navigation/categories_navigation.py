#  Copyright (c) 2022, Wahinipa LLC
from tracking.viewers.categories_viewer import CategoriesViewer


def register_categories_navigation(navigator):
    def register(task):
        endpoint = f'categories_bp.categories_{task}'
        navigator.register(CategoriesViewer, task, endpoint)

    register('create')
    register('view')
