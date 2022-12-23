# Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.linkage_handler import LinkageHandler


class UnlinkHandler(LinkageHandler):
    def action(self, root):
        self.person.unlink_from_root(root)
