from marshmallow import Schema, fields, pre_load, post_dump
from conduit.profile.serializers import ProfileSchema


class TagSchema(Schema):
    tagname = fields.Str()


class ArticleSchema(Schema):
    slug = fields.Str()
    title = fields.Str()
    description = fields.Str()
    createdAt = fields.DateTime()
    body = fields.Str()
    updatedAt = fields.DateTime()
    author = fields.Nested(ProfileSchema)
    article = fields.Nested('self', exclude=('article',), default=True, load_only=True)
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


article_schema = ArticleSchema()
articles_schema = ArticleSchemas(many=True)
