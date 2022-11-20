#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for


class ViewHandler:
    def validated_rendering(self):
        display_context = self.display_context_maker.display_context(
            self.navigator, self.viewer, self.display_attributes, self.source_inventory, self.destination_inventory)
        display_context.set_active_flavor(self.current_activity)
        if self.viewer:
            self.add_top_menu(display_context)
        return display_context.render_template(self.page_template)

    def add_top_menu(self, display_context):
        self.add_home_button(display_context)
        self.add_categories_button(display_context)
        self.add_observe_button(display_context)
        self.add_inbound_button(display_context)
        self.add_outbound_button(display_context)
        self.add_transfer_button(display_context)
        self.add_adjust_button(display_context)
        self.add_people_button(display_context)
        self.add_role_button(display_context)
        self.add_admin_button(display_context)

    def add_home_button(self, display_context):
        display_context.add_top_menu_item('Home', url_for('roots_bp.roots_view'), 'home')

    def add_categories_button(self, display_context):
        if self.root:
            display_context.add_top_menu_item('Categories', self.category_list_url, 'category')

    def add_observe_button(self, display_context):
        if self.root:
            display_context.add_top_menu_item('Find', self.observe_url, 'place', 'observe')

    def add_inbound_button(self, display_context):
        if self.root:
            display_context.add_top_menu_item('Inbound', self.inbound_url, 'place', 'inbound')

    def add_place_button(self, display_context):
        if self.root:
            display_context.add_top_menu_item('Place', self.place_url, 'place', 'place')

    def add_outbound_button(self, display_context):
        if self.root:
            display_context.add_top_menu_item('Outbound', self.outbound_url, 'place', 'outbound')

    def add_transfer_button(self, display_context):
        if self.root:
            display_context.add_top_menu_item('Transfer', self.transfer_url, 'place', 'transfer')

    def add_adjust_button(self, display_context):
        if self.root:
            display_context.add_top_menu_item('Adjust', self.adjust_url, 'place', 'adjust')

    def add_people_button(self, display_context):
        display_context.add_top_menu_item('People', self.people_url, 'people')

    def add_role_button(self, display_context):
        display_context.add_top_menu_item('Roles', self.role_url, 'role')

    def add_admin_button(self, display_context):
        if self.viewer.may_edit_database:
            display_context.add_top_menu_item('Admin', url_for('admin.index'), 'admin')
