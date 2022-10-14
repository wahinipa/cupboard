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

    def register(self, target, task, endpoint):
        self.registrations[navigator_registration_key(target, task)] = endpoint

    def endpoint(self, target, task):
        return self.registrations.get(navigator_registration_key(target, task))

    def url(self, target, task, **kwargs):
        endpoint = self.endpoint(target, task)
        if endpoint:
            identities = navigational_identities(target)
            return url_for(endpoint, **identities, **kwargs)
        else:
            return None
