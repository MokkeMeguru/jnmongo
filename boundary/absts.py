from pymongo import MongoClient
from pprint import pprint
from base import BoundaryBase
from bson.objectid import ObjectId
from typing import Dict, List


class Abst(BoundaryBase):
    """DB Boundary of Abstruct
    args:
    - client: MongoClient
    """
    def __init__(self, client: MongoClient):
        super(Abst, self).__init__(client=client)
        self.db = client['absts']
        self.dbe = self.db.absts

    def __call__(self, doc_titile: ObjectId, contents: Dict):
        """Insert a Abst
        args:
        - doc_title: ObjectId
            objectid from Keyword
        - contents: Dict
            contents json (dict)
        """
        result = self.dbe.insert_one(
            {'doc_title': doc_titile,
             'contents': contents})
        return result

    def find_object(self, doc_title: ObjectId):
        """find objectid by keyword
        args:
        - doc_title: ObjectId
           objectid from Keyword
        """
        result = self.dbe.find_one(
            {'doc_title': ObjectId})
        return result
