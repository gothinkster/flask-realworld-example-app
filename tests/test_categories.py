from flask import url_for
from datetime import datetime

class TestCategoryViews:

    def test_create_category(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        response = testapp.post_json(url_for('articles.create_category'), {
                "category": {
                    "catname": "Entertainment"
                }
            }, headers={
                'Authorization': 'Token {}'.format(token)
            })
        assert response.json['category']
        assert response.json['category']['catname'] == 'Entertainment'


    def test_get_categories(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        categories = ('Football', 'Baseball', 'Cricket')
        for category in categories:
            resp1 = testapp.post_json(url_for('articles.create_category'), {
                "category": {
                    "catname": category
                        }
                }, headers={
                 'Authorization': 'Token {}'.format(token)
                })

        resp = testapp.get(url_for('articles.fetch_all_categories'),
                            headers={
                                'Authorization': 'Token {}'.format(token)
                                }
                           )
        assert resp.json['categories']
        assert resp.json['categories'][0]['catname'] == 'Football'
        assert len(resp.json['categories']) == 3


    def test_delete_category(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        resp = testapp.post_json(url_for('articles.create_category'), {
                "category": {
                    "catname": "Entertainment"
                }
            }, headers={
                'Authorization': 'Token {}'.format(token)
            })
        response = testapp.delete(url_for('articles.remove_category', id=resp.json['category']['id']),
                            headers={
                                'Authorization': 'Token {}'.format(token)
                                }
                           )
        assert response.json['category']
        assert response.json['category']['message'] == 'category has been deleted'
        
    
    def test_edit_category(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        resps = testapp.post_json(url_for('articles.create_category'), {
                "category": {
                    "catname": "Entertainment"
                }
            }, headers={
                'Authorization': 'Token {}'.format(token)
            })
        response = testapp.patch_json(url_for('articles.edit_category', id=resps.json['category']['id']),{
            "category": {
                    "catname": "Hockey"
                }
                }, headers={
                            'Authorization': 'Token {}'.format(token)
                            }
                           )
        assert response.json['category']
        assert response.json['category']['id'] == 1
        assert response.json['category']['message'] == 'has been updated'

    
    def test_cannot_delete_nonexisting_category(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        response = testapp.delete(url_for('articles.remove_category', id=1),
        {"category": {
                    "catname": "Hockey"
                }
                }, headers={
                            'Authorization': 'Token {}'.format(token)
                            }, expect_errors=True)
        assert response.json['message'] == 'not found'
        assert response.status_int == 404
        
        
    def test_cannot_create_existing_category_(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('user.login_user'), {'user': {
            'email': user.email,
            'password': 'myprecious'
        }})

        token = str(resp.json['user']['token'])
        response = testapp.post_json(url_for('articles.create_category'), {
                "category": {
                    "catname": "Entertainment"
                }
            }, headers={
                'Authorization': 'Token {}'.format(token)
            })
        resps = testapp.post_json(url_for('articles.create_category'), {
                "category": {
                    "catname": "Entertainment"
                }
            }, headers={
                'Authorization': 'Token {}'.format(token)
            }, expect_errors=True)
        assert resps.json['message'] == 'category already exixts'
        
    
    def test_cannot_create_category_without_auth(self, testapp):
        response = testapp.post_json(url_for('articles.create_category'), {
                "category": {
                    "catname": "Entertainment"
                }
            }, headers={
                'Authorization': 'Token {}'.format("")
            }, expect_errors=True)
        assert response.status_int == 422

    def test_make_article_without_categorylist(self, testapp, user):
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
        print(resp.json)
        assert resp.json['article']['categories'] == ['uncategorized']

        
    def test_make_article_with_categorylist(self, testapp, user):
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
                "tagList": ["reactjs", "angularjs", "dragons"],
                "categories": ["Flying animals", "Informative articles"]
            }
        }, headers={
            'Authorization': 'Token {}'.format(token)
        })
        print(resp.json)
        assert resp.json['article']['categories'] == ["Flying animals", "Informative articles"]


    
