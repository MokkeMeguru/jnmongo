from typing import Dict


def get_element(d: Dict, k: str, message: str = 'this article has no title'):
    try:
        return d[k]
    except:
        raise Exception(message)
