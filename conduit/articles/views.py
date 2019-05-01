# coding: utf-8

import datetime as dt
from pprint import pprint
from flask import Blueprint, jsonify, request
from flask_apispec import marshal_with, use_kwargs
from flask_jwt_extended import current_user, jwt_required, jwt_optional
from marshmallow import fields
from conduit.extensions import db
from conduit.exceptions import InvalidUsage
from conduit.user.models import User
from .models import Article, Tags, Comment, Category
from .serializers import (article_schema, articles_schema, comment_schema,
                          comments_schema, categories_schema, category_schema)

blueprint = Blueprint('articles', __name__)


##########
# Articles
##########

@blueprint.route('/api/articles', methods=('GET',))
@jwt_optional
@use_kwargs({'tag': fields.Str(), 'author': fields.Str(),
             'favorited': fields.Str(), 'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(articles_schema)
def get_articles(tag=None, author=None, favorited=None, limit=20, offset=0):
    res = Article.query
    if tag:
        res = res.filter(Article.tagList.any(Tags.tagname == tag))
    if author:
        res = res.join(Article.author).join(User).filter(User.username == author)
    if favorited:
        res = res.join(Article.favoriters).filter(User.username == favorited)
    return res.offset(offset).limit(limit).all()


@blueprint.route('/api/articles', methods=('POST',))
@jwt_required
@use_kwargs(article_schema)
@marshal_with(article_schema)
def make_article(body, title, description, tagList=None, categories=None):
    article = Article(title=title, description=description, body=body,
                      author=current_user.profile)
    if categories is not None:
        for category in categories:
            mcategory = Category.query.filter_by(catname=category).first()
            if not mcategory:
                mcategory = Category(catname=category) 
                mcategory.save() 
                article.add_category(mcategory) 
    else:
        mcategory = Category(catname='uncategorized') 
        mcategory.save() 
        article.add_category(mcategory) 
                      
    if tagList is not None:
        for tag in tagList:
            mtag = Tags.query.filter_by(tagname=tag).first()
            if not mtag:
                mtag = Tags(tag)
                mtag.save()
            article.add_tag(mtag)
    article.save()
    return article


@blueprint.route('/api/articles/<slug>', methods=('PUT',))
@jwt_required
@use_kwargs(article_schema)
@marshal_with(article_schema)
def update_article(slug, **kwargs):
    article = Article.query.filter_by(slug=slug, author_id=current_user.profile.id).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.update(updatedAt=dt.datetime.utcnow(), **kwargs)
    article.save()
    return article


@blueprint.route('/api/articles/<slug>', methods=('DELETE',))
@jwt_required
def delete_article(slug):
    article = Article.query.filter_by(slug=slug, author_id=current_user.profile.id).first()
    article.delete()
    return '', 200


@blueprint.route('/api/articles/<slug>', methods=('GET',))
@jwt_optional
@marshal_with(article_schema)
def get_article(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    return article


@blueprint.route('/api/articles/<slug>/favorite', methods=('POST',))
@jwt_required
@marshal_with(article_schema)
def favorite_an_article(slug):
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.favourite(profile)
    article.save()
    return article


@blueprint.route('/api/articles/<slug>/favorite', methods=('DELETE',))
@jwt_required
@marshal_with(article_schema)
def unfavorite_an_article(slug):
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.unfavourite(profile)
    article.save()
    return article


@blueprint.route('/api/articles/feed', methods=('GET',))
@jwt_required
@use_kwargs({'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(articles_schema)
def articles_feed(limit=20, offset=0):
    return Article.query.join(current_user.profile.follows). \
        order_by(Article.createdAt.desc()).offset(offset).limit(limit).all()


######
# Tags
######

@blueprint.route('/api/tags', methods=('GET',))
def get_tags():
    return jsonify({'tags': [tag.tagname for tag in Tags.query.all()]})


##########
# Comments
##########


@blueprint.route('/api/articles/<slug>/comments', methods=('GET',))
@marshal_with(comments_schema)
def get_comments(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    return article.comments


@blueprint.route('/api/articles/<slug>/comments', methods=('POST',))
@jwt_required
@use_kwargs(comment_schema)
@marshal_with(comment_schema)
def make_comment_on_article(slug, body, **kwargs):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    comment = Comment(article, current_user.profile, body, **kwargs)
    comment.save()
    return comment


@blueprint.route('/api/articles/<slug>/comments/<cid>', methods=('DELETE',))
@jwt_required
def delete_comment_on_article(slug, cid):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()

    comment = article.comments.filter_by(id=cid, author=current_user.profile).first()
    comment.delete()
    return '', 200
   
##########
#category
#########

@blueprint.route('/api/categories', methods=['POST'])
@jwt_required
def create_category():
    json_data = request.get_json() 
    if not request.json or not 'category' in json_data:
        return jsonify({'message': 'field is empty, please cross check', 'status': 404}), 404
    data, errors = category_schema.load(json_data)
    category = Category.query.filter_by(catname=data['catname']).first()
    if not category:
        category_name = Category(catname=data['catname'])
        db.session.add(category_name)
        db.session.commit()
        data, errors = category_schema.dump(category_name)
        print(data)
        return jsonify(data) ,201
    return jsonify({'message': 'category already exixts'}), 404

@blueprint.route('/api/categories/<int:id>', methods=['DELETE'])
@jwt_required
def remove_category(id):
    category = Category.query.filter_by(id=id).first()
    if not category:
        return jsonify({'message': 'not found', 'status': 404}), 404 
    db.session.delete(category)
    return jsonify({'category':{'id': id , 'message': 'category has been deleted'}, 'status': 200}), 200


@blueprint.route('/api/categories/<int:id>/category', methods=['PATCH'])
@jwt_required
def edit_category(id):
        json_data = request.get_json()
        data, errors = category_schema.load(json_data)
        category = Category.query.filter_by(id=id).first()
        if not category:
             return jsonify({'message': 'not found', 'status': 404}) ,404
        else:
            category.update(catname=data['catname'])
            db.session.add(category)
            db.session.commit()
            return jsonify({'category': {'id':id, 'message': \
            'has been updated'}, 'status': 200}), 200


@blueprint.route('/api/categories', methods=['GET'])
@jwt_required
def fetch_all_categories():
    categories = Category.query.all()
    if not categories :
        return jsonify({'message': ' not found', 'status' : 404}) ,404
    data, errors = categories_schema.dump(categories)
    return jsonify(data), 200



