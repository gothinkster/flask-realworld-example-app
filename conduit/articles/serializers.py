# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump, post_load
import json
from .models import Category

from conduit.profile.serializers import ProfileSchema


class TagSchema(Schema):
    tagname = fields.Str()


class ArticleSchema(Schema):
    slug = fields.Str()
    title = fields.Str()
    description = fields.Str()
    createdAt = fields.DateTime()
    body = fields.Str()
    updatedAt = fields.DateTime(dump_only=True)
    author = fields.Nested(ProfileSchema)
    article = fields.Nested('self', exclude=('article',), default=True, load_only=True)
    categories = fields.List(fields.Str())
    tagList = fields.List(fields.Str())
    favoritesCount = fields.Int(dump_only=True)
    favorited = fields.Bool(dump_only=True)

    @pre_load
    def make_article(self, data):
        return data['article']

    @post_dump
    def dump_article(self, data):
        data['author'] = data['author']['profile']
        return {'article': data}

    class Meta:
        strict = True


class ArticleSchemas(ArticleSchema):

    @post_dump
    def dump_article(self, data):
        data['author'] = data['author']['profile']
        return data

    @post_dump(pass_many=True)
    def dump_articles(self, data, many):
        return {'articles': data, 'articlesCount': len(data)}


class CommentSchema(Schema):
    createdAt = fields.DateTime()
    body = fields.Str()
    updatedAt = fields.DateTime(dump_only=True)
    author = fields.Nested(ProfileSchema)
    id = fields.Int()

    # for the envelope
    comment = fields.Nested('self', exclude=('comment',), default=True, load_only=True)

    @pre_load
    def make_comment(self, data):
        return data['comment']

    @post_dump
    def dump_comment(self, data):
        data['author'] = data['author']['profile']
        return {'comment': data}

    class Meta:
        strict = True


class CommentsSchema(CommentSchema):

    @post_dump
    def dump_comment(self, data):
        data['author'] = data['author']['profile']
        return data

    @post_dump(pass_many=True)
    def make_comment(self, data, many):
        return {'comments': data}



class CategorySchema(Schema):
    catname = fields.Str()
    id = fields.Int()
    

    # for the envelope
    category = fields.Nested('self', exclude=('category',), default=True, load_only=True)

    @pre_load
    def make_category(self, data):
        if not data:
            return None 
        return data['category']

    @post_dump(pass_many=True)
    def dump_category(self, data, many):
        key = 'categories' if many else 'category'
        return  {
            key : data
        }
            

    class Meta:
        strict = True

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
article_schema = ArticleSchema()
articles_schema = ArticleSchemas(many=True)
comment_schema = CommentSchema()
comments_schema = CommentsSchema(many=True)
