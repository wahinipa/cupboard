#  Copyright (c) 2022, Wahinipa LLC
from tracking.modelling.refinement_model import add_refinement
from tracking.page_handlers.refinement_base_handler import RefinementBaseHandler


class RefinementAddHandler(RefinementBaseHandler):

    def change_refinement(self):
        add_refinement(self.thing, self.category)
