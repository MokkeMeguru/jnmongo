import os
import argparse
from getpass import getpass
from pathlib import Path
from pprint import pprint
import json
from flask import jsonify

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
        result = {
            "Content-Type" : "application/json",
            "body" : result
        }
        return jsonify(result)


server = Server()
app = Flask(__name__)

@app.route("/list")
def title_list():
    return server.doc_list()

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
