from pymongo import MongoClient
from pprint import pprint
from base import BoundaryBase
from bson.objectid import ObjectId
from typing import List, Dict


class Related_Words(BoundaryBase):
    """DB Boundary of Related Words
    """
    def __init__(self, client: MongoClient):
        super(Related_Words, self).__init__(client=client)
        self.db = client['related_words']
        self.dbe = self.db.conte

    def __call__(self,
                 doc_title: ObjectId,
                 texts: List[str],
                 contents: Dict):
        """Insert Related Words
        args:
        - doc_title: ObjectId
            objectid from Keyword
        - texts: List[str]
            extracted related word list
        - contents:
            un-extracted related words
        """
        result = self.dbe.insert_one(
            {'doc_title': doc_title,
             'texts': texts,
             'contents': contents})
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

    def update_objects(self, doc_title: ObjectId, m: Dict):
        """update object
        args:
        - doc_title: ObjectId
           objectid from Keyword
        - m: Dict
            update instructions
        """
        result = self.dbe.update_one(
            m.update({'doc_title': doc_title}))
        return result
