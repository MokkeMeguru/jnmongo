from datetime import datetime
from typing import Dict, List

from bson.objectid import ObjectId
from pymongo import MongoClient

from boundary.base import BoundaryBase


class Related_Words(BoundaryBase):
    """DB Boundary of Related Words
    Attributes:
        client (MongoClient): MongoDB's client
    """

    def __init__(self, client: MongoClient):
        """
        Args:
            client (MongoClient): MongoDB's client
        """
        super(Related_Words, self).__init__(client=client)
        self.db_collection = self.db.related_words

    def insert(self,
               doc_title: ObjectId,
               words: List,
               contents: Dict):
        """Insert Related Words
        Args:
            doc_title (ObjectId): objectid from Keyword
            words (List[ObjectId]): extracted related word list
            contents (Dict): non-extracted related words
        """
        now = datetime.utcnow()
        result = self.db_collection.update_one(
            {"_id": doc_title},
            {"$set": {"contents": contents},
             "$setOnInsert": {
                 "_id": doc_title,
                 "insertion_date": now},
             "$addToSet": {
                 "words": {"$each": words}
             }},
            True, False
        )
        return result

    def find_objects(self, doc_title: ObjectId):
        """find object by objectid
        Args:
            doc_title (ObjectId): objectid from Keyword
        """
        result = self.db_collection.find_one(
            {'_id': doc_title})
        return result
