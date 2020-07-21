from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import app_config
from flask_cors import CORS


db = SQLAlchemy()

api = Api()

from resources import register_routes
from handlers import register_error_handlers


def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    import logging
    logging.basicConfig(
        level=logging.getLevelName(app.config.get("LOG_LEVEL"))
    )

    logger = logging.getLogger("App")
    logger.info("Starting app!")

    register_routes(api)
    register_error_handlers(app)

    api.init_app(app)
    db.init_app(app)

    CORS(app, origins=["*"], supports_credentials=True)
    app.config['CORS_HEADERS'] = 'Content-Type'

    return app
