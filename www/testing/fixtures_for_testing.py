# Copyright 2022 Wahinipa LLC

import pytest


class PretendApplication:
    def __init__(self):
        self.blueprints = {}

    def register_blueprint(self, blueprint, url_prefix=None):
        blueprint_name = blueprint.name
        self.blueprints[blueprint_name] = {
            "blueprint": blueprint,
            "url_prefix": url_prefix
        }


@pytest.fixture
def pretend_application():
    return PretendApplication()
