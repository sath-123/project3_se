import config
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    environment_configuration = os.environ['CONFIGURATION_SETUP']
    app.config.from_object(environment_configuration)

    db.init_app(app)

    with app.app_context():
        from .order_api import order_api_blueprint
        app.register_blueprint(order_api_blueprint)
        db.create_all()

    return app

