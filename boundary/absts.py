from typing import Dict

from bson.objectid import ObjectId
from pymongo import MongoClient

from boundary.base import BoundaryBase


class Abst(BoundaryBase):
    """DB Boundary of Abstruct
    Attributes:
        client (MongoClient): MongoDB's client
    """

    def __init__(self, client: MongoClient):
        """
        Args:
            client (MongoClient): MongoDB's client
        """
        super(Abst, self).__init__(client=client)
        self.db_collection = self.db.absts
        self.db_collection.creat_index('doc_title', unique=True)

    def insert(self, doc_titile: ObjectId, contents: Dict):
        """Insert a Abstruct
        Args:
            doc_title (ObjectId): objectid from Keyword
            contents (Dict): jsoned contents
        Note:
            Avoid conflictiog, we believe latest document
            is correct. if insert existing contents,
            this methid will update it.
        """
        result = self.db_collection.update_one({
            'doc_title': doc_titile,
            'contents': contents
        }, upsert=True)
        return result

    def find_object(self, doc_title: ObjectId):
        """find objectid by document
        Args:
            doc_title (ObjectId): document's index
        """
        result = self.db_collection.find_one({'doc_title': ObjectId})
        return result
