#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.refinement_model import remove_refinement
from tracking.page_handlers.refinement_base_handler import RefinementBaseHandler


class RefinementRemoveHandler(RefinementBaseHandler):

    def change_refinement(self):
        remove_refinement(self.thing, self.category)
