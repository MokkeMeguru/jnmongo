import datetime
import pprint
from typing import Dict, List, Union

import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient

default_doc = {
    "author": "Mike",
    "text":"My first blog post!",
    "tags": ["mognodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()
}

default_docs = [
    {"author": "Mike",
     "text": "Another post!",
     "tags": ["bulk", "insert"],
     "date": datetime.datetime(2009, 11, 12, 11, 14)},
    {"author": "Eliot",
     "title": "MongoDB is fun",
     "text": "and pretty easy too!",
     "date": datetime.datetime(2009, 11, 10, 10, 45)}
]


default_query = {
    "author": "Mike"
}

extra_query = {
    "date": {"$lt": datetime.datetime(2009, 11, 12, 12)}
}

class BeginMongo:
    def __init__(self, password: str):
        if not password:
            password = getpass()
        self.client = MongoClient(
            host='localhost',
            port=27017,
            password=password,
            username="root"
        )
        self.testdb = self.client.test_database

    def insert(self, doc: Dict=default_doc):
        posts = self.testdb.posts
        post_id = posts.insert_one(doc).inserted_id
        return post_id

    def insert_many(self, docs: List[Dict]=default_docs):
        result = self.testdb.posts.insert_many(docs)
        return result.inserted_ids

    def find_by_query(self, query: Dict=default_query,
                      projection:dict={},
                      one: bool=True):
        if one:
            return self.testdb.posts.find_one(
                filter=query,
                projection=projection)
        else:
            return self.testdb.posts.find(
                filter=query,
                projection=projection)

    def find_by_Id(self, object_id: Union[str, ObjectId],
                   projection:dict={},
                   one: bool=True):
        if isinstance(object_id, str):
            object_id = ObjectId(object_id)
        return self.testdb.posts.find_one(
            filter={"_id": object_id},
            projection=projection)

    def create_index(self, index_key: str):
        return self.testdb.posts.create_index(index_key)


def main():
    password = getpass()
    beginmongo = BeginMongo(password)


if __name__ == '__main__':
    main()
