# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag
from conduit.extensions import db
from flask_migrate import Migrate
from conduit.app import create_app
from conduit.settings import DevConfig, ProdConfig
CONFIG = DevConfig if get_debug_flag() else ProdConfig
from conduit.articles.views import create_category

app = create_app(DevConfig)
app_context = app.app_context()
app_context.push()
db.create_all()
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run()