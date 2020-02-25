from datetime import datetime
from pprint import pprint

from pymongo import MongoClient

from boundary.base import BoundaryBase


class DocKeywords(BoundaryBase):
    """DB Boundary of Keyword of Documents
    args:
    - client: MongoClient
    note:
         this class creates the db table, 'keywords' by documents' id
    """

    def __init__(self, client: MongoClient):
        super(DocKeywords, self).__init__(client=client)
        self.db = client['dockeywords']
        self.dbe = self.db.dockeywords

    def __call__(self, doc_title, keyword):
        """Insert a keyword
        args:
        - doc_title: object_id
        - keyword: object_id
        string keyword like a word such as 'Google'
        returns
        - result
        """
        now = datetime.utcnow()
        result = self.dbe.update(
            {"doc_title": doc_title},
            {"$setOnInsert": {
                "doc_title": doc_title,
                "insertion_date": now},
             "$addToSet":   {"keywords": keyword,
                             "last_update_date": now}},
            True, False)
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

    def find_object(self, doc_title):
        """find objectid by keyword
        args:
            doc_title: objecId of document
        returns:
        - result: ObjectId
            the objectid of the keyword
        """
        result = self.dbe.find_one({'doc_title':  doc_title})
        return result["keywords"]
