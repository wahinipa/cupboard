#  Copyright (c) 2022, Wahinipa LLC
from flask import url_for


def navigator_registration_key(target, task):
    """
    Calculate a key that is unique to the target class and task.
    Examples: 'Place:create' 'User:update'
    :param target:
    :param task:
    :return:
    """
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
    """
    Tracks two important navigational mappings:
        What is the endpoint (aka routing method) for a specific target and task?
        For a given endpoint, what are the Roles that allow the user to access or use that endpoint?

    When creating or accessing the mappings, the target can be either a class or an instance of that class.
    Either way, the class name is used in the registration.

    """
    def __init__(self):
        self.registrations = {}
        self.role_names = {}

    def register(self, target, task, endpoint, role_names):
        """
        Add these to the mappings.
        :param target:
        :param task:
        :param endpoint:
        :param role_names:
        :return:
        """
        self.registrations[navigator_registration_key(target, task)] = endpoint
        self.role_names[endpoint] = role_names

    def endpoint(self, target, task):
        return self.registrations.get(navigator_registration_key(target, task))

    def endpoint_role_names(self, endpoint):
        return self.role_names[endpoint]

