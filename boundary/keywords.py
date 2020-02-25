from datetime import datetime
from pprint import pprint

from pymongo import MongoClient

from boundary.base import BoundaryBase


class Keyword(BoundaryBase):
    """DB Boundary of Keyword
    args:
    - client: MongoClient
    note:
         this class creates the db table, 'keywords'
    """

    def __init__(self, client: MongoClient):
        super(Keyword, self).__init__(client=client)
        self.db = client['keywords']
        self.dbe = self.db.keywords

    def __call__(self, keyword: str):
        """Insert a keyword
        args:
        - keyword: str
        string keyword like a word such as 'Google'
        returns
        - result
        """
        now = datetime.utcnow()
        result= self.dbe.update(
            {"keyword": keyword},
            {"$setOnInsert": {
                "keyword": keyword,
                "insertion_date": now},
             "$set": {"last_update_date": now}},
            True, False
        )
        return result

    def get_by_id(self, objectId):
        """get name by objectId
        args:
            objectId: mongodb 's objectId
        returns:
            keywords (str):  keyword word
        """
        results = self.dbe.find_one({"_id": objectId})
        return results

    def find_object(self, keyword: str):
        """find objectid by keyword
        args:
        - keyword: str
            keyword word
        returns:
        - result: ObjectId
            the objectid of the keyword
        """
        result = self.dbe.find_one({'keyword':  keyword})
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
