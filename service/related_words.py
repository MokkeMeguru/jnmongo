from boundary import related_words
from typing import Dict, List
from service.utils import get_element
from itertools import chain

def walk_words(d) -> List:
    if type(d) is dict:
        v = d.get('content', [])
        words = walk_words(v)
        return words
    elif type(d) is str:
        return set([d])
    elif type(d) is list:
        acc = set()
        for i in d:
            acc = acc | walk_words(i)
        return acc
    else:
        return acc


def extract_item(article: Dict):
    """extract related words from raw article
    args:
    - article: Dict
    returns:
    - title: str
    - related_words: Dict
    related words's section
    """
    title = get_element(article, 'title')
    raw_related_words = article.get('related_words', [])
    _related_words = walk_words(raw_related_words)
    return title, list(_related_words)
