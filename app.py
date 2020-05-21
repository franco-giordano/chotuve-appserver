from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import app_config

import os

# TODO logging!

db = SQLAlchemy()


def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    import logging
    logging.basicConfig(
        level=logging.getLevelName(app.config.get("LOG_LEVEL"))
    )

    logger = logging.getLogger("App")
    logger.info("Starting app!")

    db.init_app(app)

    return app

