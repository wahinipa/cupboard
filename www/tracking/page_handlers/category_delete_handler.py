#  Copyright (c) 2022, Wahinipa LLC

from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.page_handlers.target_delete_handler import TargetDeleteHandler
from tracking.viewers.categories_model import Categories


class CategoryDeleteHandler(CategoryBaseHandler, TargetDeleteHandler):

    @property
    def delete_redirect_url(self):
        return self.navigator.url(Categories, 'view')
