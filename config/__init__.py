import os


class Config(object):
    """ Default settings"""
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    TESTING = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    SERVICE_NAME = 'flask_api_service'

    # Data base configuration
    MONGODB_URI = 'mongodb://localhost:27017'

    # Basic authentication
    USERNAME = "test"
    PASSWORD = "1eBf&3x8"
