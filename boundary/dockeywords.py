from datetime import datetime

from bson.objectid import ObjectId
from pymongo import MongoClient

from boundary.base import BoundaryBase


class DocKeywords(BoundaryBase):
    """DB Boundary of Keyword of Documents
    Attributes:
        client (MongoClient): MongoDB's client
    """

    def __init__(self, client: MongoClient):
        super(DocKeywords, self).__init__(client=client)
        self.db_collection = self.db.dockeywords

    def insert(self, doc_title: ObjectId, keyword: ObjectId()):
        """Insert a keyword
        Args:
            doc_title (ObjectId): document's ObjectId
            keyword (ObjectId):
                related keywords such as "Web" by "Google"
        """
        now = datetime.utcnow()
        result = self.db_collection.update_one(filter={"_id": doc_title},
                                               update={
                                                   "$setOnInsert": {
                                                       "_id": doc_title,
                                                       "insertion_date": now
                                                   },
                                                   "$addToSet": {
                                                       "keywords": keyword,
                                                       "last_update_date": now
                                                   }
                                               },
                                               upsert=True)
        return result

    def find_object(self, doc_title: ObjectId):
        """find objectid by keyword
        Args:
            doc_title (ObjectId): objecId of document
        Returns:
            result (ObjectId): the objectid of the keyword
        """
        result = self.db_collection.find_one({'_id': doc_title})
        return result["keywords"]
