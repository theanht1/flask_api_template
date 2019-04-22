import datetime

from . import mongo_db


class BaseMongoModel:
    __collection__ = ''

    @classmethod
    def get_collection(cls):
        return mongo_db[cls.__collection__]

    @classmethod
    def save(cls, doc):
        doc['created'] = datetime.datetime.utcnow()
        return mongo_db[cls.__collection__].insert_one(doc).inserted_id

    @classmethod
    def update(cls, query_filter, query_update):
        if query_update.get('$set') and not query_update.get('$set').get('updated'):
            query_update['$set']['updated'] = datetime.datetime.utcnow()

        return mongo_db[cls.__collection__].update_one(
            query_filter,
            query_update
        )

    @classmethod
    def find_by_id(cls, object_id):
        return mongo_db[cls.__collection__].find_one({"_id": object_id})
