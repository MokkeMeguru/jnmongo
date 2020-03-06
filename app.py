import argparse
from getpass import getpass
from pathlib import Path
from pprint import pprint

from pymongo import MongoClient

from boundary.absts import Abst
from boundary.contents import Content
from boundary.dockeywords import DocKeywords
from boundary.keywords import Keyword
from boundary.related_words import Related_Words
from parse import json_parser
from service import absts, contents, related_words, utils


class Saver:
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

    def save_json(self, article):
        # parse json
        title = utils.get_element(article, 'title')
        rrw, rw = related_words.extract_item(article)

        keywords = article.get('keywords', [])
        abstruct, _, left = absts.extract_abstruct(article['article'])
        sections, _ = contents.SectionParser()(left)
        sections = [section.to_dict() for section in sections]

        # check title
        self.keyword_db.insert(title)
        title_objectid = self.keyword_db.find_object(title)
        title = self.keyword_db.get_by_id(title_objectid)
        print(title_objectid, '->', title)

        # check keywords
        pprint(keywords)
        for keyword in keywords:
            self.keyword_db.insert(keyword)
        for keyword in keywords:
            self.dockeywords_db.insert(
                title_objectid,
                self.keyword_db.find_object(keyword))

        # for keyword in rw:
        #     self.relatedwords_db(title_objectid, )
        #         title_objectid, self.keyword_db.find_object(keyword))

        # pprint(rw)
        # pprint(abstruct)
        # pprint(sections)


def main(json_path: str):
    path = Path(json_path)
    article = json_parser.read_json(path)
    saver = Saver()
    saver.save_json(article)
    return saver


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--json_path',
        help='jsons\'s path generated by niconico-parser via web',
        type=str)
    args = parser.parse_args(args=['--json_path', '三枝明那.json'])
    main(args.json_path)
    # main("三枝明那.json")
