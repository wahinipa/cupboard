#  Copyright (c) 2022, Wahinipa LLC

class TargetHandler:
    def __init__(self, target):
        self.target = target

    @property
    def objects_are_valid(self):
        return self.target and self.base_says_objects_are_valid()
