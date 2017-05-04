# coding: utf-8

from flask import Blueprint
from flask_apispec import marshal_with
from .models import UserProfile
from flask_jwt import current_identity, jwt_required
from conduit.user.models import User
from conduit.user.serializers import user_schema
from .serializers import profile_schema
from conduit.exceptions import InvalidUsage, USER_NOT_FOUND


blueprint = Blueprint('profiles', __name__)


@blueprint.route('/api/profiles/<username>', methods=('GET',))
@marshal_with(profile_schema)
def get_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise InvalidUsage(**USER_NOT_FOUND)
    # set the other attributes
    userprofile = user.profile
    userprofile.following = False
    # if logged in check if user is following.
    if current_identity:
        userprofile.following = current_identity.profile.is_following(user.profile)
    for attr, value in user_schema.dump(user).data['user'].items():
        setattr(userprofile, attr, value)
    return userprofile


@blueprint.route('/api/profiles/<username>/follow', methods=('POST',))
@jwt_required()
@marshal_with(profile_schema)
def follow_user(username):
    profile1 = User.query.filter_by(username=username).first().profile
    profile2 = current_identity.profile
    profile2.follow(profile1)
    profile1.following = profile2.is_following(profile1)
    for attr, value in user_schema.dump(profile1.user).data['user'].items():
        setattr(profile1, attr, value)
    return profile1


@blueprint.route('/api/profiles/<username>/follow', methods=('DELETE',))
@jwt_required()
@marshal_with(profile_schema)
def unfollow_user(username):
    profile1 = User.query.filter_by(username=username).first().profile
    profile2 = current_identity.profile
    profile2.unfollow(profile1)
    profile1.following = profile2.is_following(profile1)
    for attr, value in user_schema.dump(profile1.user).data['user'].items():
        setattr(profile1, attr, value)
    return profile1
