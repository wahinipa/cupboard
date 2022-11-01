#  Copyright (c) 2022, Wahinipa LLC
from flask import redirect

from tracking import database
from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.viewers.categories_model import Categories


class CategoryDeleteHandler(CategoryBaseHandler):

    def validated_rendering(self):
        redirect_url = self.navigator.url(Categories, 'view')
        database.session.delete(self.category)
        database.session.commit()
        return redirect(redirect_url)

    @property
    def viewer_has_permission(self):
        return self.category.may_delete(self.viewer)
