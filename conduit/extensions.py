# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""

from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT
from flask_cors import CORS


bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
cors = CORS()

from conduit.utils import authenticate, jwt_identity  # noqa

jwt = JWT(authentication_handler=authenticate, identity_handler=jwt_identity)
