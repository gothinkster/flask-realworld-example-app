# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from conduit.user.models import User  # noqa


def jwt_identity(payload):
    return User.get_by_id(payload)


def identity_loader(user):
    return user.id
