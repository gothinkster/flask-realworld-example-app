# coding: utf-8

from flask import Blueprint
from flask_apispec import marshal_with
from flask_jwt import current_identity, jwt_required
from conduit.user.models import User
from .serializers import profile_schema
from conduit.exceptions import InvalidUsage, USER_NOT_FOUND
from conduit.utils import jwt_optional
from conduit.extensions import cors


blueprint = Blueprint('profiles', __name__)
cors.init_app(blueprint)


@blueprint.route('/api/profiles/<username>', methods=('GET',))
@jwt_optional()
@marshal_with(profile_schema)
def get_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage(**USER_NOT_FOUND)
    return user.profile


@blueprint.route('/api/profiles/<username>/follow', methods=('POST',))
@jwt_required()
@marshal_with(profile_schema)
def follow_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage(**USER_NOT_FOUND)
    current_identity.profile.follow(user.profile)
    current_identity.profile.save()
    return user.profile


@blueprint.route('/api/profiles/<username>/follow', methods=('DELETE',))
@jwt_required()
@marshal_with(profile_schema)
def unfollow_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage(**USER_NOT_FOUND)
    current_identity.profile.unfollow(user.profile)
    current_identity.profile.save()
    return user.profile
