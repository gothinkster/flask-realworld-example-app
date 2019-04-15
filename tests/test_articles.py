# coding: utf-8

from flask import url_for
from datetime import datetime

class TestArticleViews:

    def test_get_articles_by_author(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        for _ in range(2):
            testapp.post_json(url_for('articles.make_article'), {
                "article": {
                    "title": "How to train your dragon {}".format(_),
                    "description": "Ever wonder how?",
                    "body": "You have to believe",
                    "tagList": ["reactjs", "angularjs", "dragons"]
                }
            }, headers={
                'Authorization': 'Token {}'.format(token)
            })

        resp = testapp.get(url_for('articles.get_articles', author=user.username))
        assert len(resp.json['articles']) == 2

    def test_favorite_an_article(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        resp1 = testapp.post_json(url_for('articles.make_article'), {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "You have to believe",
                "tagList": ["reactjs", "angularjs", "dragons"]
            }
        }, headers={
            'Authorization': 'Token {}'.format(token)
        })

        resp = testapp.post(url_for('articles.favorite_an_article',
                                    slug=resp1.json['article']['slug']),
                            headers={
                                'Authorization': 'Token {}'.format(token)
                                }
                           )
        assert resp.json['article']['favorited']

    def test_get_articles_by_favoriter(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        for _ in range(2):
            testapp.post_json(url_for('articles.make_article'), {
                "article": {
                    "title": "How to train your dragon {}".format(_),
                    "description": "Ever wonder how?",
                    "body": "You have to believe",
                    "tagList": ["reactjs", "angularjs", "dragons"]
                }
            }, headers={
                'Authorization': 'Token {}'.format(token)
            })

        resp = testapp.get(url_for('articles.get_articles', author=user.username))
        assert len(resp.json['articles']) == 2

    def test_make_article(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        resp = testapp.post_json(url_for('articles.make_article'), {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "You have to believe",
                "tagList": ["reactjs", "angularjs", "dragons"]
            }
        }, headers={
            'Authorization': 'Token {}'.format(token)
        })
        assert resp.json['article']['author']['email'] == user.email
        assert resp.json['article']['body'] == 'You have to believe'

    def test_make_comment_correct_schema(self, testapp, user):
        from conduit.profile.serializers import profile_schema
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        resp = testapp.post_json(url_for('articles.make_article'), {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "You have to believe",
                "tagList": ["reactjs", "angularjs", "dragons"]
            }
        }, headers={
            'Authorization': 'Token {}'.format(token)
        })
        slug = resp.json['article']['slug']
        # make a comment
        resp = testapp.post_json(url_for('articles.make_comment_on_article', slug=slug), {
            "comment": {
                "createdAt": datetime.now().isoformat(),
                "body": "You have to believe",
            }
        }, headers={
            'Authorization': 'Token {}'.format(token)
        })

        # check
        authorp = resp.json['comment']['author']
        del authorp['following']
        assert profile_schema.dump(user).data['profile'] == authorp

    def test_make_category(self, testapp, user):
        resp = testapp.post_json(url_for('articles.make_category'),
            {"title": "New Category"})
        assert resp.json['category']['title'] == "New Category"

    def test_list_all_categories(self, testapp, user):
        category1 = testapp.post_json(url_for('articles.make_category'),
            {"title": "New Category1"})
        category2 = testapp.post_json(url_for('articles.make_category'),
            {"title": "New Category2"})
        resp = testapp.get(url_for('articles.get_categories'))
        assert len(resp.json['categories']) == 2

    def test_get_category_by_id(self, testapp, user):
        category1 = testapp.post_json(url_for('articles.make_category'),
            {"title": "New Category1"})
        resp = testapp.get(url_for('articles.get_category', id=1))
        assert resp.json['category']['title'] == "New Category1"

    def test_edit_category(self, testapp, user):
        category1 = testapp.post_json(url_for('articles.make_category'),
            {"title": "New Category1"})
        resp = testapp.put(url_for('articles.edit_category', id=1), {
            'title': 'New Title',
        })
        assert resp.json['category']['title'] == "New Title"

    def test_delete_category(self, testapp, user):
        category1 = testapp.post_json(url_for('articles.make_category'),
            {"title": "New Category1"})
        resp = testapp.delete(url_for('articles.delete_category', id=1))
        assert resp.status_code == 200

    def test_cannot_delete_category_with_children(self, testapp, user):
        category = testapp.post_json(url_for('articles.make_category'),
            {"title": "New Category1", "parent_id": 1})
        resp = testapp.delete(url_for('articles.delete_category', id=1), expect_errors=True)
        assert resp.status_code == 409
        assert resp.json['errors']['body'][0] == "Can not delete category with children"
