from datetime import datetime
from pprint import pprint

from bson.objectid import ObjectId
from pymongo import MongoClient

from boundary.base import BoundaryBase


class Keyword(BoundaryBase):
    """DB Boundary of Keyword
    Attributes:
        client (MongoClient): MongoDB's client
    Note:
        This class creates the db table, 'keywords'
    """

    def __init__(self, client: MongoClient):
        """
        Args:
            client (MongoClient): MongoDB's client
        """
        super(Keyword, self).__init__(client=client)
        self.db_collection = self.db.keywords
        self.db_collection.create_index('keyword', unique=True)

    def insert(self, keyword: str):
        """Insert a keyword
        Args:
            keyword (str): string keyword like a word such as 'Google'
        """
        now = datetime.utcnow()
        result = self.db_collection.update_one(
            filter={"keyword": keyword},
            update={
                "$setOnInsert": {
                    "keyword": keyword,
                    "insertion_date": now,
                    "reference": 0},
                "$set": {"last_update_date": now},
            },
            upsert=True
        )
        self.db_collection.update_one(
            filter={"keyword": keyword},
            update={
                "$inc": {"reference": 1}
            })
        return result

    def get_by_id(self, objectId: ObjectId):
        """get name by objectId
        Args:
            objectId (ObjectId): mongodb 's objectId
        Returns:
            keywords (str): keyword word
        """
        results = self.db_collection.find_one({"_id": objectId})
        return results

    def find_object(self, keyword: str):
        """find objectid by keyword
        Args:
            keyword (str): keyword word
        Returns:
            result (ObjectId): the objectid of the keyword
        """
        result = self.db_collection.find_one({'keyword':  keyword})
        if len(result) == 0:
            self.insert(keyword)
            self.find_object(Keyword)
        return result["_id"]


def test():
    client = MongoClient('127.0.0.1', 27017)
    keyword_db = Keyword(client)
    pprint(keyword_db("ニコニコ大百科"))
    pprint(keyword_db.all)
    object_id = keyword_db.find_objct("ニコニコ大百科")
    pprint(object_id)
    pprint(keyword_db.get(object_id)["keyword"])
    pprint(len(keyword_db))
    keyword_db.reset()
    pprint(len(keyword_db))


if __name__ == '__main__':
    test()
