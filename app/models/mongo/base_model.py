import datetime

from . import mongo_db
from bson import ObjectId
from bson.errors import InvalidId


class BaseMongoModel:
    """
    Common model for handling mongodb database
    """
    __collection__ = ''  # Mongodb collection

    @classmethod
    def get_collection(cls):
        """
        Get the mongodb collection
        :return:
        """
        return mongo_db[cls.__collection__]

    @classmethod
    def save(cls, doc):
        """
        Save one doc to the collection

        :param doc: <dict> Document data
        :return:
        """
        doc['created'] = datetime.datetime.utcnow()
        return mongo_db[cls.__collection__].insert_one(doc).inserted_id

    @classmethod
    def update(cls, query_filter, query_update):
        """
        Update one doc in the collection

        :param query_filter: <dict> Filter condition
        :param query_update: <dict> Updating data
        :return:
        """
        if query_update.get('$set') and not query_update.get('$set').get('updated'):
            query_update['$set']['updated'] = datetime.datetime.utcnow()

        return mongo_db[cls.__collection__].update_one(
            query_filter,
            query_update
        )

    @classmethod
    def find_by_id(cls, object_id):
        """
        Get one document from the collection by looking for its id

        :param object_id: <string> String that presents bson id of the document
        :return: <object or None> Mongodb object
        """
        try:
            return mongo_db[cls.__collection__].find_one({"_id": ObjectId(object_id)})
        except InvalidId:
            # TODO: Log the exception
            print('Invalid bson id: {}'.format(object_id))
            return None
