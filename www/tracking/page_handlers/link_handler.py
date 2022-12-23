# Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.linkage_handler import LinkageHandler


class LinkHandler(LinkageHandler):
    def action(self, root):
        self.person.link_to_root(root)
