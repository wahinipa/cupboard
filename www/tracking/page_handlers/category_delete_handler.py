#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.role_models import Role
from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.page_handlers.target_delete_handler import TargetDeleteHandler
from tracking.viewers.categories_viewer import CategoriesViewer


class CategoryDeleteHandler(CategoryBaseHandler, TargetDeleteHandler):
    required_role_name = Role.admin_role_name

    @property
    def delete_redirect_url(self):
        return self.navigator.target_url(CategoriesViewer, 'view')
