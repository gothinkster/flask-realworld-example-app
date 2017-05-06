# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump


class UserSchema(Schema):
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    bio = fields.Str()
    image = fields.Url()
    token = fields.Str()
    # ugly hack.
    user = fields.Nested('self', exclude=('user',), default=True, load_only=True)

    @pre_load
    def make_user(self, data):
        data = {key: value for key, value in data['user'].items() if value != ''}
        return data

    @post_dump
    def dump_user(self, data):
        return {'user': data}

    class Meta:
        strict = True


user_schema = UserSchema()
user_schemas = UserSchema(many=True)
