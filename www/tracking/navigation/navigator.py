#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for


def navigator_registration_key(target, task):
    mark = navigational_mark(target)
    return f'{mark}:{task}'


def target_class(target):
    if isinstance(target, type):
        return target
    else:
        return target.__class__


def navigational_mark(target):
    return target_class(target).__name__


def navigational_identities(target):
    if isinstance(target, type):
        return {}
    else:
        return target.identities


class Navigator:
    def __init__(self):
        self.registrations = {}
        self.role_names = {}

    def register(self, target, task, endpoint, role_names):
        self.registrations[navigator_registration_key(target, task)] = endpoint
        self.role_names[endpoint] = role_names

    def endpoint(self, target, task):
        return self.registrations.get(navigator_registration_key(target, task))

    def endpoint_role_names(self, endpoint):
        return self.role_names[endpoint]

