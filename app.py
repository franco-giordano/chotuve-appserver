from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from config import app_config
from flask_cors import CORS
from flask_restful.utils import cors



db = SQLAlchemy()

api = Api()

from resources import register_routes
from handlers import register_error_handlers

from daos.http_daos import httpDAO

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

    CORS(app, origins=["*"], send_wildcard=True)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}

    api.decorators = [
            cors.crossdomain(
                origin='*',
                methods = ['GET', 'PUT', 'PATCH', 'POST', 'DELETE', 'OPTIONS'],
                attach_to_all = True,
                automatic_options = False
            )
    ]

        
    @app.after_request
    def after_request(response):

        httpDAO.add_entry(path=request.path,
                        method=request.method,
                        response_code=response.status_code,
                        client_ip=request.remote_addr)

        return response


    return app
