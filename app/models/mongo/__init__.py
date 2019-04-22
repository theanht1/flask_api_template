from flask import current_app
from pymongo import MongoClient

# Init database
mongo = MongoClient(current_app.config['MONGO_DATABASE_URI'])
mongo_db = mongo[current_app.config['MONGO_DATABASE_NAME']]
