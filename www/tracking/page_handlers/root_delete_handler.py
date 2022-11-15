#  Copyright (c) 2022, Wahinipa LLC
from tracking.page_handlers.root_base_handler import RootBaseHandler
from tracking.page_handlers.target_delete_handler import TargetDeleteHandler
from tracking.viewers.roots_viewer import RootsViewer


class RootDeleteHandler(RootBaseHandler, TargetDeleteHandler):

    @property
    def delete_redirect_url(self):
        return self.navigator.target_url(RootsViewer, 'view')
