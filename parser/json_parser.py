from memory_profiler import profile
import sys
sys.path.append('../../jnmongo')
import json
from pathlib import Path
from service import related_words
from pprint import pprint

def read_json(path: Path):
    with path.open(mode='r', encoding='utf-8') as f:
        article = json.load(f)
    return article


def main():
    path =  Path('/home/meguru/Github/jnmongo') / Path('三枝明那.json')
    article = read_json(path)
    title, _related_words = related_words.extract_item(article)
    pprint(_related_words)

if __name__ == '__main__':
    main()
