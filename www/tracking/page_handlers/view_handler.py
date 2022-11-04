#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for


class ViewHandler:
    def validated_rendering(self):
        display_context = self.display_context_maker.display_context(self.navigator, self.viewer,
                                                                     self.display_attributes)
        display_context.set_active_flavor(self.active_flavor)
        if self.viewer:
            self.add_top_menu(display_context)
        return display_context.render_template(self.page_template)

    def add_top_menu(self, display_context):
        self.add_home_button(display_context)
        self.add_categories_button(display_context)
        self.add_place_button(display_context)
        self.add_people_button(display_context)
        self.add_admin_button(display_context)

    @property
    def viewer_has_permission(self):
        return self.target.may_be_observed(self.viewer)

    def add_home_button(self, display_context):
        display_context.add_top_menu_item('Home', url_for('roots_bp.roots_view'), 'home')

    def add_categories_button(self, display_context):
        if self.root:
            display_context.add_top_menu_item('Categories', self.category_list_url, 'category')

    def add_place_button(self, display_context):
        if self.root:
            display_context.add_top_menu_item('Place', self.place_url, 'place')

    def add_people_button(self, display_context):
        display_context.add_top_menu_item('People', url_for('people_bp.people_list'), 'people')

    def add_admin_button(self, display_context):
        if self.viewer.may_edit_database:
            display_context.add_top_menu_item('Admin', url_for('admin.index'), 'admin')
