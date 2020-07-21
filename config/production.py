from config import Config


class ProductionConfig(Config):
    ENV = "production"
    MONGODB_URI = ""
