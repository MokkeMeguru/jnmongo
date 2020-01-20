from pymongo import MongoClient
from pprint import pprint
from base import BoundaryBase
from bson.objectid import ObjectId
from typing import List, Dict


class Content(BoundaryBase):
    """DB Boundary of Content
    """
    def __init__(self, client: MongoClient):
        super(Content, self).__init__(client=client)
        self.db = client['contents']
        self.dbe = self.db.contents

    def __call__(self,
                 doc_title: ObjectId,
                 child_titles: List[str],
                 contents: Dict):
        """Insert a Content
        args:
        - doc_title: ObjectId
           objectid from Keyword
        - child_titles: List[str]
           subtitle words
        - contents: Dict
           contents json (dict)
        """
        result = self.dbe.insert_one(
            {'doc_title': doc_title,
             'child_titles': child_titles,
             'contents': contents})
        return result

    def find_objects(self, doc_title: ObjectId, child_titles: List[str] = []):
        """find objectid by some elements
        args:
        - doc_title: ObjectId
            objectid from keywod
        - child_titles: List[str]
            subtitle words (default [])
        returns:
        - results: List[Dict]
           candidate objects
        """
        if len(child_titles) != 0:
            result = self.dbe.find(
                {'doc_title': doc_title,
                 'child_titles': {"$in": child_titles},
                })
        else:
            result = self.dbe.find(
                {'doc_title': doc_title})
        return list(result)


def test():
    client = MongoClient('127.0.0.1', 27017)
    # stub
    from keywords import Keyword
    keyword_db = Keyword(client)
    keyword_db("ニコニコ大百科")
    object_id = keyword_db.find_objct("ニコニコ大百科")

    content_db = Content(client)
    content_db(object_id, ["概要"],
               {"type": None, "content": ["ここは概要"]})
    content_db(object_id, ["概要", "プロフィール"],
               {"type": None, "content": ["ここは概要の中のプロフィール"]})
    content_db(object_id, ["プロフィール"],
               {"type": None, "content": ["ここはプロフィール"]})
    content_db(object_id, ["関連項目"],
               {"type": None, "content": ["ここは関連項目"]})

    print('search: ', ["概要"])
    pprint(content_db.find_objects(object_id, ["概要"]))

    print('search: ', ["プロフィール"])
    pprint(content_db.find_objects(object_id, ["プロフィール"]))

    print('search: ', ["概要", "プロフィール"])
    pprint(content_db.find_objects(object_id, ["概要", "プロフィール"]))

    print('search: ', ["関連項目"])
    pprint(content_db.find_objects(object_id, ["関連項目"]))

    print('search: ', ["関連商品"])
    pprint(content_db.find_objects(object_id, ["関連商品"]))

    print('show all')
    pprint(content_db.all)
    keyword_db.reset()
    content_db.reset()

if __name__ == '__main__':
    test()
