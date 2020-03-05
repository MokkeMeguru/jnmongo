from pprint import pprint
from typing import Dict, List

from bson.objectid import ObjectId
from pymongo import MongoClient

from boundary.base import BoundaryBase


class Content(BoundaryBase):
    """DB Boundary of Abstruct
    Attributes:
        client (MongoClient): MongoDB's client
    """

    def __init__(self, client: MongoClient):
        """
        Args:
            client (MongoClient): MongoDB's client
        """
        super(Content, self).__init__(client=client)
        self.db_collection = self.db.contents

    def insert(self, doc_title: ObjectId, child_titles: List[str],
               contents: Dict):
        """Insert a Content
        Args:
            doc_title (ObjectId): objectid from Keyword
            child_titles (List[ObjectId]) (subtitle): words's ObjectId
            contents (Dict) (jsoned): contents
        """
        result = self.db_collection.insert_one({
            'doc_title': doc_title,
            'child_titles': child_titles,
            'contents': contents
        })
        return result

    def find_objects(self,
                     doc_title: ObjectId,
                     child_titles: List[ObjectId] = []):
        """find objectid by some elements
        Args:
            doc_title (ObjectId): objectid from keywod
            child_titles (List[ObjectId]): subtitle words (default [])
        returns:
            results (List[Dict]): candidate objects
        """
        if len(child_titles) != 0:
            result = self.db_collection.find({
                'doc_title': doc_title,
                'child_titles': {
                    "$in": child_titles
                }})
        elif doc_title is None:
            result = self.db_collection.find({
                'child_titles': {"$in": child_titles}
            })
        else:
            result = self.db_collection.find({'doc_title': doc_title})
        return list(result)


def test():
    client = MongoClient('127.0.0.1', 27017)
    # stub
    from keywords import Keyword
    keyword_db = Keyword(client)
    keyword_db("ニコニコ大百科")
    object_id = keyword_db.find_objct("ニコニコ大百科")

    content_db = Content(client)
    content_db(object_id, ["概要"], {"type": None, "content": ["ここは概要"]})
    content_db(object_id, ["概要", "プロフィール"], {
        "type": None,
        "content": ["ここは概要の中のプロフィール"]
    })
    content_db(object_id, ["プロフィール"], {"type": None, "content": ["ここはプロフィール"]})
    content_db(object_id, ["関連項目"], {"type": None, "content": ["ここは関連項目"]})

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
