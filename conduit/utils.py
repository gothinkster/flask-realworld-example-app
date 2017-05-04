# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from conduit.user.models import User


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def jwt_identity(payload):
    user_id = payload['identity']
    return User.get_by_id(user_id)


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
