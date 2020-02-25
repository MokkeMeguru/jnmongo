from datetime import datetime
from pprint import pprint
from typing import Dict, List

from bson.objectid import ObjectId
from pymongo import MongoClient

from boundary.base import BoundaryBase


class Related_Words(BoundaryBase):
    """DB Boundary of Related Words
    """

    def __init__(self, client: MongoClient):
        super(Related_Words, self).__init__(client=client)
        self.db = client['related_words']
        self.dbe = self.db.rw

    def __call__(self,
                 doc_title: ObjectId,
                 words: List,
                 contents: Dict):
        """Insert Related Words
        args:
        - doc_title: ObjectId
            objectid from Keyword
        - words: List[ObjectId]
            extracted related word list
        - contents:
            un-extracted related words
        """
        now = datetime.utcnow()
        result = self.dbe.update(
            {"doc_title": doc_title},
            {"$set": {"contents": contents},
             "$setOnInsert": {
                 "doc_title": doc_title,
                 "insertion_date": now},
             "$addToSet": {
                 "words": {"$each": words}
             }},
            True, False
        )
        return result

    def find_objects(self, doc_title: ObjectId):
        """find object by objectid
        args:
        - doc_title: ObjectId
           objectid from Keyword
        """
        result = self.dbe.find_one(
            {'doc_title': doc_title})
        return result
