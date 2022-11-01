#  Copyright (c) 2022, Wahinipa LLC
from flask_login import current_user

from tracking.contexts.card_display_attributes import dual_view_childrens_attributes
from tracking.page_handlers.category_base_handler import CategoryBaseHandler
from tracking.viewers.categories_model import Categories


class CategoryViewHandler(CategoryBaseHandler):

    def validated_rendering(self):
        display_attributes = {
            'description': True,
            'children': [self.category, self.thing, self.thing_specification],
            'children_attributes': dual_view_childrens_attributes(thing=self.thing),
        }
        place_url = self.navigator.url(self.root, 'view')
        category_list_url = self.navigator.url(Categories, 'view')
        return self.root.display_context(self.navigator, current_user, display_attributes).render_template(
            "pages/category_view.j2", category_list_url=category_list_url, place_url=place_url,
            active_flavor='category')

    @property
    def viewer_has_permission(self):
        return self.category.may_be_observed(self.viewer)
