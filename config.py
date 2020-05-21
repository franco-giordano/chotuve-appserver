import os

class Config(object):
    DEBUG = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL','sqlite://')



class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    LOG_LEVEL = "INFO"


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
