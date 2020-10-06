# -*- coding: utf-8 -*-
from flask import Flask
import config


def create_app():
    # Create the Flask app.
    app = Flask(__name__)

    # Load application configurations
    load_config(app)
    init_modules(app)

    return app


def init_modules(app):
    # Import a module / component using its blueprint handler variable
    from app.views import basic_page
    from app.views import test_page
    from app.views import api_endpoint

    # Register blueprint(s)
    app.register_blueprint(basic_page)
    app.register_blueprint(test_page)
    app.register_blueprint(api_endpoint)


def load_config(app):
    # Add Server Port to App config
    app.config['SERVER_PORT'] = config.SERVER_PORT

    # Add Secret Key
    app.config['FN_FLASK_SECRET_KEY'] = config.FN_FLASK_SECRET_KEY

    # Add SSL certifcate/key paths
    app.config['SSL'] = (config.CERT, config.KEY)
