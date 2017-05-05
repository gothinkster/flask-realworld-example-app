# coding: utf-8

from flask import Blueprint, jsonify
from flask_apispec import marshal_with, use_kwargs
from .serializers import article_schema, articles_schema
from flask_jwt import jwt_required, current_identity
from .models import Article, Tags
from sqlalchemy.exc import IntegrityError
from conduit.user.models import User
from conduit.exceptions import InvalidUsage, UNKONW_ERROR, ARTICLE_NOT_FOUND
from marshmallow import fields
from conduit.utils import jwt_optional


blueprint = Blueprint('articles', __name__)


@blueprint.route('/api/articles', methods=('GET',))
@jwt_optional()
@use_kwargs({'tag': fields.Str(), 'author': fields.Str(),
             'favorited': fields.Str(), 'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(articles_schema)
def get_articles(tag=None, author=None, favorited=None, limit=20, offset=0):
    res = Article.query
    if tag:
        res = res.filter(Article.tagList.any(Tags.tagname == tag))
    if author:
        res = res.join(Article.author).filter(User.username == author)
    if favorited:
        res = res.join(Article.favoriters).filter(User.username == favorited)
    print(current_identity)
    return res.offset(offset).limit(limit).all()


@blueprint.route('/api/articles', methods=('POST',))
@jwt_required()
@use_kwargs(article_schema)
@marshal_with(article_schema)
def make_article(body, title, description, tagList=None):
    try:
        article = Article(title=title, description=description, body=body,
                          author=current_identity.profile)
    except IntegrityError as e:
        raise InvalidUsage(**UNKONW_ERROR)
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
@jwt_required()
@use_kwargs(article_schema)
@marshal_with(article_schema)
def update_article(slug, **kwargs):
    article = Article.query.filter_by(slug=slug, author_id=current_identity.profile.id).first()
    if not article:
        raise InvalidUsage(**ARTICLE_NOT_FOUND)
    article.update(**kwargs)
    article.save()
    return article


@blueprint.route('/api/articles/<slug>', methods=('DELETE',))
@jwt_required()
def delete_article(slug):
    article = Article.query.filter_by(slug=slug, author_id=current_identity.profile.id).first()
    article.delete()
    return '', 200


@blueprint.route('/api/articles/<slug>', methods=('GET',))
@jwt_optional()
@marshal_with(article_schema)
def get_article(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage(**ARTICLE_NOT_FOUND)
    return article


@blueprint.route('/api/articles/<slug>/favorite', methods=('POST',))
@jwt_required()
@marshal_with(article_schema)
def favorite_an_article(slug):
    profile = current_identity.profile
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage(**ARTICLE_NOT_FOUND)
    article.favourite(profile)
    article.save()
    return article


@blueprint.route('/api/articles/feed', methods=('GET',))
@jwt_required()
@use_kwargs({'limit': fields.Int(), 'offset': fields.Int()})
@marshal_with(articles_schema)
def articles_feed(limit=20, offset=0):
    return current_identity.profile.follows.join(Article).order_by(Article.createdAt.desc())\
                                           .offset(offset).limit(limit).all()


######
# Tags
######

@blueprint.route('/api/tags', methods=('GET',))
def get_tags():
    return jsonify({'tags': [tag.tagname for tag in Tags.query.all()]})
