# coding: utf-8

from flask import url_for
from werkzeug.exceptions import NotFound
from .factories import UserFactory
from conduit.exceptions import USER_NOT_FOUND


def _register_user(testapp, **kwargs):
    return testapp.post_json(url_for('user.register_user'), {
          "user": {
              "email": 'foo@bar.com',
              "username": 'foobar',
              "password": 'myprecious'
          }}, **kwargs)


class TestProfile:

    def test_get_profile_not_loggedin(self, testapp):
        _register_user(testapp)
        resp = testapp.get(url_for('profiles.get_profile', username='foobar'))
        assert resp.json['profile']['email'] == 'foo@bar.com'
        assert resp.json['profile']['following'] is False

    def test_get_profile_not_existing(self, testapp):
        resp = testapp.get(url_for('profiles.get_profile', username='foobar'), expect_errors=True)
        assert resp.status_int == 404
        assert resp.json == USER_NOT_FOUND['message']

    def test_follow_user(self, testapp, user):
        resp = _register_user(testapp)
        token = resp.json['user']['token']
        resp = testapp.post(url_for('profiles.follow_user', username=user.username), headers={
            'Authorization': 'Token %s' % token
        })
        resp.json['profile']['following'] is True

    def test_unfollow_user(self, testapp, user):
        resp = _register_user(testapp)
        token = resp.json['user']['token']
        resp = testapp.delete(url_for('profiles.unfollow_user', username=user.username), headers={
            'Authorization': 'Token %s' % token
        })
        resp.json['profile']['following'] is False
