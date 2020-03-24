import logging
import os
import argparse
from getpass import getpass
from pathlib import Path
from pprint import pprint
import json
from flask import jsonify, request

from pymongo import MongoClient

from boundary.absts import Abst
from boundary.contents import Content
from boundary.dockeywords import DocKeywords
from boundary.keywords import Keyword
from boundary.related_words import Related_Words
from parse import json_parser
from service import absts, contents, related_words, utils
from flask import Flask

class Server:
    def __init__(self):
        self.setup_db()

    def setup_db(self):
        password = getpass()
        client = MongoClient(host='127.0.0.1',
                             port=27017,
                             username="root",
                             password=password)
        self.abst_db = Abst(client)
        self.content_db = Content(client)
        self.keyword_db = Keyword(client)
        self.dockeywords_db = DocKeywords(client)
        self.relatedwords_db = Related_Words(client)

    def doc_list(self):
        result = [self.keyword_db.get_by_id(v['_id'], projection={"keyword": 1})["keyword"] 
                    for v in self.abst_db.db_collection.find(projection={"_id": 1})]
        return result

    def related_words(self, doc_title: str):
        doc_title = self.keyword_db.find_object(doc_title, not_found_error=True)
        if doc_title is None:
            return []
        result = [self.keyword_db.get_by_id(v, projection={"keyword" : 1, "_id": 0})["keyword"]
                 for v in self.relatedwords_db.find_objects(doc_title)["words"]]
        return result

    def contents(self, doc_title: str):
        doc_title = self.keyword_db.find_object(doc_title, not_found_error=True)
        if doc_title is None:
            return []
        result = []
        for content in self.content_db.find_objects(doc_title):
            content.pop("doc_title")
            content.pop ("_id")
            result.append (content)
        return result

server = Server()
app = Flask(__name__)

def resulty(result):
    result =  {
        "Content-Type": "application/json",
        "body": result
    }
    return jsonify(result)

@app.route("/list")
def title_list():
    return resulty(server.doc_list())

@app.route("/related_words")
def related_words():
    doc_title = request.args.get("doc_title")
    if doc_title is None:
        logging.WARN("doc_title is not found at request /related_words")
        return resulty([])
    return resulty(server.related_words(doc_title))

@app.route("/contents")
def contents():
    doc_title = request.args.get("doc_title")
    if doc_title is None:
        logging.WARN("doc_title is not found at request /contents")
        return resulty ([])
    return resulty(server.contents(doc_title))

def main(args):
    app.run(host=os.getenv("APP_ADDRESS", 'localhost'), port=args.port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--port',
        type=int,
        default="8085"
    )

    args = parser.parse_args()
    main(args)
    # args = parser.parse_args(args=['store', '--json_folder', 'resources'])
    # main(args.json_path)
    # main("三枝明那.json")
