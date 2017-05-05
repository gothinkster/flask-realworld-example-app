# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from conduit.user.models import User
from conduit.profile.models import UserProfile
from conduit.articles.models import Article, Tags

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

    def test_unfollow_user(self):
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
        p1.unfollow(p2)
        assert p1.is_following(p2) is False

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


@pytest.mark.usefixtures('db')
class TestArticles:
    def test_create_article(self, user):
        u1 = user.get()
        article = Article(u1.profile, 'title', 'some body', description='some')
        article.save()
        assert article.author.user is u1

    def test_favorite_an_article(self):
        u1 = User('foo', 'foo@bar.com')
        u1.save()
        p1 = UserProfile(u1)
        p1.save()
        article = Article(p1, 'title', 'some body', description='some')
        article.save()
        assert article.favourite(u1.profile) is True
        assert article.is_favourite(u1.profile) is True

    def test_unfavorite_an_article(self):
        u1 = User('foo', 'foo@bar.com')
        u1.save()
        p1 = UserProfile(u1)
        p1.save()

        u2 = User('foo1', 'fo1o@bar.com')
        u2.save()
        p2 = UserProfile(u2)
        p2.save()

        article = Article(p1, 'title', 'some body', description='some')
        article.save()
        assert article.favourite(p1) is True
        assert article.unfavourite(p1) is True
        assert article.is_favourite(p1) is False

    def test_add_tag(self, user):
        user = user.get()
        article = Article(user.profile, 'title', 'some body', description='some')
        article.save()
        t = Tags(tagname='python')
        t1 = Tags(tagname='flask')
        assert article.add_tag(t) is True
        assert article.add_tag(t1) is True
        assert len(article.tagList) == 2

    def test_remove_tag(self, user):
        user = user.get()
        article = Article(user.profile, 'title', 'some body', description='some')
        article.save()
        t1 = Tags(tagname='flask')
        assert article.add_tag(t1) is True
        assert article.remove_tag(t1) is True
        assert len(article.tagList) == 0
