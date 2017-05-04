# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint
from .serializers import user_schema
from .models import User
from conduit.profile.models import UserProfile
from flask_jwt import current_identity, jwt_required, _default_jwt_encode_handler
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import IntegrityError
from conduit.exceptions import USER_ALREADY_REGISTERED, InvalidUsage, USER_NOT_FOUND

blueprint = Blueprint('user', __name__)


@blueprint.route('/api/users', methods=('POST',))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def register_user(username, password, email, **kwargs):
    try:
        userprofile = UserProfile(User(username, email, password=password, **kwargs).save()).save()
    except IntegrityError:
        raise InvalidUsage(**USER_ALREADY_REGISTERED)
    userprofile.user.token = _default_jwt_encode_handler(userprofile.user).decode('utf-8')
    return userprofile.user


@blueprint.route('/api/users/login', methods=('POST',))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def login_user(email, password, **kwargs):
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        user.token = _default_jwt_encode_handler(user).decode('utf-8')
        return user
    else:
        raise InvalidUsage(**USER_NOT_FOUND)


@blueprint.route('/api/user', methods=('GET',))
@jwt_required()
@marshal_with(user_schema)
def get_user():
    token = _default_jwt_encode_handler(current_identity).decode('utf-8')
    current_identity.token = token
    return current_identity


@blueprint.route('/api/user', methods=('PUT',))
@jwt_required()
@use_kwargs(user_schema)
@marshal_with(user_schema)
def update_user(**kwargs):
    print(kwargs)
    user = current_identity
    # take in consideration the password
    password = kwargs.pop('password', None)
    if password:
        user.set_password(password)
    user.update(**kwargs)
    user.token = _default_jwt_encode_handler(user).decode('utf-8')
    return user
