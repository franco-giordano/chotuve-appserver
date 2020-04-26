from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import app_config

import os


db = SQLAlchemy()


def create_app(config_name):

    app = Flask(__name__)
        

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app

