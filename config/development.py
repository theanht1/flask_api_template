from config import Config


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
