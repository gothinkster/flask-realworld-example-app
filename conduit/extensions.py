# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model


class CRUDMixin(Model):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


bcrypt = Bcrypt()
db = SQLAlchemy(model_class=CRUDMixin)
migrate = Migrate()
cache = Cache()
cors = CORS()

from conduit.utils import jwt_identity, identity_loader  # noqa

jwt = JWTManager()
jwt.user_loader_callback_loader(jwt_identity)
jwt.user_identity_loader(identity_loader)
