from pprint import pprint
from typing import Dict, List

from bson.objectid import ObjectId
from pymongo import MongoClient

from boundary.base import BoundaryBase


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
