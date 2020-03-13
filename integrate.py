from parse import json_parser
from service import utils, related_words, absts, contents

from boundary.absts import Abst
from boundary.contents import Content
from boundary.dockeywords import DocKeywords
from boundary.keywords import Keyword
from boundary.related_words import Related_Words
from service.contents import SectionTree

from pymongo import MongoClient
from bson.objectid import ObjectId
from getpass import getpass
from pathlib import Path
import pandas as pd

from typing import List, Union, Tuple, Dict


class ParsedArticle:
    def __init__(self, file: Path):
        self.raw_data = json_parser.read_json(file)
        self.title = utils.get_element(self.raw_data, "title")
        self.title_head = utils.get_element(self.raw_data, "title-head")
        self.keywords = utils.get_element(
            self.raw_data, "keywords", 
            message="this article has no keywords")       
        self.raw_related_words, self.related_words = related_words.extract_item(self.raw_data)
        self.related_words_len = len(self.related_words)
        self.abstruct, self.sections = self.parse_article()

    def parse_article(self):
        article = utils.get_element(
            self.raw_data, "article", message="this article has no body")
        import copy
        abstruct, _ ,left = absts.extract_abstruct(article)
        sections, _= contents.SectionParser().parse(left)
        return abstruct, sections


class Boundary:
    def __init__(self, 
            username: str="root", password: str ="passwd", 
            host: str="127.0.0.1", port: int=27017):
        client = MongoClient(host=host, 
            port=port, username=username, password=password)
        self.abst_db = Abst(client)
        self.content_db = Content(client)
        self.keyword_db = Keyword(client)
        self.dockeywords_db = DocKeywords(client)
        self.relatedwords_db = Related_Words(client)
    
    @property
    def info(self):
        return {
            "abst": len(self.abst_db),
            "content": len(self.content_db),
            "keyword": len(self.keyword_db),
            "dockeywords": len(self.dockeywords_db),
            "relatedwords": len(self.relatedwords_db)}
    
    def __repr__(self):
        return str(self.info)
    
    def reset(self):
        self.abst_db.reset()
        self.content_db.reset()
        self.keyword_db.reset()
        self.dockeywords_db.reset()
        self.relatedwords_db.reset()

    # Insert

    def insert_keyword(
        self, keyword: Union[str, List[str], Tuple[str]]):
        if type(keyword) is str:
            self.keyword_db.insert(keyword)
        elif type(keyword) in [list, tuple]:
            [self.keyword_db.insert(k) for k in keyword]
        else:
            raise NotImplementedError()

    def insert_dockeywords(
        self, title: Union[str, ObjectId],
        keywords: Union[List[str], List[ObjectId]]):
        if type(title) is str:
            title = self.get_keyword(title)
        if len(keywords) != 0 and type(keywords[0]) is str:
            keywords = self.get_keyword(keywords)
        self.dockeywords_db.insert(title, keywords)

    def insert_relatedwords(
        self, title: Union[str, ObjectId],
        related_words: Union[List[str], List[ObjectId]],
        raw_related_words: Dict):
        if type(title) is str:
            title = self.get_keyword(title)
        if len(related_words) != 0 and type(related_words[0]) is str:
            related_words = self.get_keyword(related_words)
        self.relatedwords_db.insert(
            title,
            related_words,
            raw_related_words)
    def insert_abstruct(
        self, title: Union[str, ObjectId], abstruct: Dict):
        if type(title) is str:
            title = self.get_keyword(title)
        self.abst_db.insert(title, abstruct)

    def insert_sections(
        self, title: Union[str, ObjectId], 
        sections: List[SectionTree]):
        if type(title) is str:
            title = self.get_keyword(title)
        for sec in sections:
            self.content_db.insert(
                title,
                sec.titles,
                sec.contents)
    
    def insert_article(
        self, article: ParsedArticle):
        self.insert_keyword(article.title)
        self.insert_keyword(article.related_words)
        self.insert_keyword(article.keywords)
        for sec in article.sections:
            self.insert_keyword(sec.titles)
        self.insert_dockeywords(
            article.title,
            article.keywords)
        self.insert_relatedwords(
            article.title,
            article.related_words,
            article.raw_related_words)
        self.insert_abstruct(
            article.title,
            article.abstruct)
        self.insert_sections(
            article.title,
            article.sections)

    # Get

    def get_keyword(
        self, 
        keyword: Union[str, List[str], ObjectId, List[ObjectId]]):
        # an instance
        if type(keyword) is str:
            return self.keyword_db.find_object(keyword)
        elif type(keyword) is ObjectId:
            return self.keyword_db.get_by_id(keyword)
        # list of instance
        elif type(keyword) is list:
            if type(keyword[0]) is str:
                return [self.keyword_db.find_object(k) 
                        for k in keyword]
            elif type(keyword[0]) is ObjectId:
                return [self.keyword_db.get_by_id(k) 
                        for k in keyword]
        else:
            raise NotImplementedError()

    def get_section(
        self, 
        title: Union[str, ObjectId], 
        child_titles: Union[List[str], List[ObjectId]],
        keywords: Union[List[str], List[ObjectId]]):
        
        if len(keywords) != 0:
            if type(keywords[0]) is str:
                keywords = self.get_keyword(keywords)
        
            if type(keywords[0]) is ObjectId:
                return self.content_db.find_objects(title, candidates=keywords)
        
        if len(child_titles) != 0:
            return self.content_db.find_objects(title, child_titles=child_titles)
        

        else:
            raise NotImplementedError()