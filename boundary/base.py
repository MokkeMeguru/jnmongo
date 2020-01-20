from pymongo import MongoClient
from pprint import pprint
from bson.json_util import dumps
from bson.objectid import ObjectId
from abc import ABC, abstractmethod
from pymongo.database import Database


class BoundaryBase(ABC):
    def __init__(self, client: MongoClient):
        self.client = client

    @abstractmethod
    def __call__(self, m):
        return m

    def get(self, object_id: ObjectId):
        """find object by objectid
        args:
        - object_id: ObjectId
           objectid
        returns:
        - result: dict
            the object of the objectid
        """
        result = self.dbe.find_one({'_id': object_id})
        return result

    @property
    def all(self):
        """get all objects
        returns:
        - result: list
           list of objects
        """
        result = self.dbe.find()
        return list(result)

    @property
    def jsoned_all(self):
        """get all objects as json
        returns:
        - result: list
           jsoned list of objects
        """
        result = self.dbe.find()
        return dumps(result)

    def reset(self):
        """reset db
        """
        self.dbe.delete_many({})

    def __len__(self):
        return self.dbe.count_documents({})
