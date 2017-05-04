# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from conduit.user.models import User
from conduit.profile.models import UserProfile


from .factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User('foo', 'foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.check_password('myprecious')

    def test_check_password(self):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com',
                           password='foobarbaz123')
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('barfoobaz') is False


@pytest.mark.usefixtures('db')
class TestProfile:

    def test_follow_user(self):
        u1 = User('foo', 'foo@bar.com')
        u1.save()
        u2 = User('foo1', 'foo1@bar.com')
        u2.save()
        p1 = UserProfile(u1)
        p2 = UserProfile(u2)
        p1.save()
        p2.save()
        p1.follow(p2)
        assert p1.is_following(p2) is True

    def test_follow_self(self):
        u1 = User('foo', 'foo@bar.com')
        u1.save()
        p1 = UserProfile(u1)
        p1.save()
        assert p1.follow(p1) is False

    def test_unfollow_self(self):
        u1 = User('foo', 'foo@bar.com')
        u1.save()
        p1 = UserProfile(u1)
        assert p1.unfollow(p1) is False
