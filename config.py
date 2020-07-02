import os


class Config(object):
    DEBUG = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    LOG_LEVEL = "INFO"
    PROPAGATE_EXCEPTIONS = True


class TestConfig(Config):
    TESTING = True
    LOG_LEVEL = "DEBUG"


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig
}
