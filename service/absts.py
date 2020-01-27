from typing import Dict
import regex


def extract_abstruct(article, next_flag = True, left=[]):
    if not next_flag:
        return article, next_flag, left

    if type(article) is list:
        acc = []
        for item in article:
            item, next_flag, left = extract_abstruct(item, next_flag, left)
            if item is None or item == []:
                continue
            if next_flag:
                acc.append(item)
            else:
                left.append(item)
        return acc, next_flag, left

    elif type(article) is dict:
        attr = article.get('attrs', {})
        if attr and attr.get('id', '') == 'page-menu':
            return None, next_flag, left
        tag = article['tag']
        tag_content = article['content'][0]
        if tag == 'h2' and not regex.match(r'概要', tag_content):
            # regex.match(r'h\d', tag) and len(tag) == 2:
            return article, False, left
        else:
            return article, next_flag, left

    elif type(article) is str:
        return article, next_flag, left

    else:
        return article, next_flag, left
