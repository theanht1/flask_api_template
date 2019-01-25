import os


class Config(object):
    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    JSONIFY_PRETTYPRINT_REGULAR = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    TESTING = True


configs = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}

configuration = configs.get(os.getenv('SEO_PLATFORM', 'development'))()
