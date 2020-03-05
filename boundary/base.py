from abc import ABC

from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient


class BoundaryBase(ABC):
    def __init__(self, client: MongoClient):
        """
        Args:
            client (MongoClient): MongoDB's client
        """
        self.client = client
        self.db = client.niconico

    def get(self, object_id: ObjectId):
        """find object by objectid
        Args:
            object_id (ObjectId): it's objectid

        Returns:
            result (Dict): the object of the objectid
        """
        result = self.db_collection.find_one({'_id': object_id})
        return result

    @property
    def all(self):
        """get all objects
        Returns:
            result (List): list of objects
        """
        result = self.db_collection.find()
        return list(result)

    @property
    def jsoned_all(self):
        """get all objects as json
        Returns:
            result (list): jsoned list of objects
        """
        result = self.db_collection.find()
        return dumps(result)

    def reset(self):
        """reset db
        """
        self.db_collection.delete_many({})

    def __len__(self):
        return self.db_collection.count_documents({})
