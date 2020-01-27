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
    - rrw: Dict
    related words's section
    - rw: list
    extracted related words
    """
    rrw = article.get('related_words', [])
    rw = walk_words(rrw)
    return rrw, list(rw)
