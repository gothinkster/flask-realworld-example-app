# -*- coding: utf-8 -*-
"""Create an application instance."""
from flask.helpers import get_debug_flag
from flask import Flask

from conduit.app import create_app
from conduit.settings import DevConfig, ProdConfig

CONFIG = DevConfig if get_debug_flag() else ProdConfig

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World! V1.0'


if __name__ == '__main__':
    app.debug = True
    app.run()
