import sys
sys.path.append('../')
from memory_profiler import profile
import json
from pathlib import Path
from service import related_words, utils, absts
import argparse
from pprint import pprint



def read_json(path: Path):
    with path.open(mode='r', encoding='utf-8') as f:
        article = json.load(f)
    return article


def main(json_path: str):
    path = Path(json_path)
    article = read_json(path)
    title = utils.get_element(article, 'title')
    rrw, rw = related_words.extract_item(article)
    keywords = article.get('keywords', [])
    abstruct, _, left = absts.extract_abstruct(article['article'])
    pprint(title)
    pprint(keywords)
    pprint(rw)
    pprint(abstruct)
    pprint(left)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--json_path',
        help='jsons\'s path generated by niconico-parser via web',
        type=str)
    args = parser.parse_args(args=['--json_path', '../三枝明那.json'])
    main(args.json_path)
