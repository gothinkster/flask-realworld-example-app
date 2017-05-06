# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint
from .serializers import user_schema
from .models import User
from conduit.profile.models import UserProfile
from flask_jwt import current_identity, jwt_required
from flask_apispec import use_kwargs, marshal_with
from sqlalchemy.exc import IntegrityError
from conduit.exceptions import USER_ALREADY_REGISTERED, InvalidUsage, USER_NOT_FOUND
from conduit.utils import jwt_optional
from conduit.database import db
from conduit.extensions import cors


blueprint = Blueprint('user', __name__)
cors.init_app(blueprint)


@blueprint.route('/api/users', methods=('POST',))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def register_user(username, password, email, **kwargs):
    try:
        userprofile = UserProfile(User(username, email, password=password, **kwargs).save()).save()
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage(**USER_ALREADY_REGISTERED)
    return userprofile.user


@blueprint.route('/api/users/login', methods=('POST',))
@jwt_optional()
@use_kwargs(user_schema)
@marshal_with(user_schema)
def login_user(email, password, **kwargs):
    user = User.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        print(user.token)
        return user
    else:
        raise InvalidUsage(**USER_NOT_FOUND)


@blueprint.route('/api/user', methods=('GET',))
@jwt_required()
@marshal_with(user_schema)
def get_user():
    return current_identity


@blueprint.route('/api/user', methods=('PUT',))
@jwt_required()
@use_kwargs(user_schema)
@marshal_with(user_schema)
def update_user(**kwargs):
    user = current_identity
    # take in consideration the password
    password = kwargs.pop('password', None)
    if password:
        user.set_password(password)
    user.update(**kwargs)
    return user
