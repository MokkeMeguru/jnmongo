from typing import List, Dict
import regex

# source
# h2-1
# content1
# h2-2
# content2
#   |-  h2-3
#   |- content3
#          |-  h3-1
#          |- content4
#  |- content5
# h2-3
#  |- content6
# h3-3
#  |- content7

# to
# h2-1 content1 | h2-1
# h2-2 content2 | h2-2
# h2-3 content3 content5 | h2-2 h2-3
# h3-1 content4 | h2-2 h2-3 h3-1
# h2-3 content6 | h2-3
# h3-3 content7 | h3-3


class ChildrenReduccer:
    def __init__(self, tree_contents=[], contents=[], tag_list=[]):
        self.tree_contents = tree_contents
        self.contents: List = contents
        self.tag_list: List[str] = tag_list

    def call(self, article: Dict):
        if type(article) is dict:
            tag = article['tag']
            tag_name = article['content'][0]
            if regex.match(r'h\d', tag) and len(tag) == 2:
                self.tree_contents.append(
                    {'child_titles': self.tag_list,
                     'contents': self.contents})
                self.tag_list.append(tag_name)



def parse_children(
        article, acc: List = [],
        contents: List = [],
        child_titles: List = [],
        storage: List = [],
        proceeds: List = []):
    if type(article) is dict:
        tag = article['tag']
        tag_content = article['content'][0]
        if regex.match(r'h\d', tag) and len(tag) == 2:
            child_titles.append(tag_content)
            if len(contents) > 0:
                storage.append(contents)
                contents.append(article)
                return [], contents, child_titles, storage, proceeds
            else:
                return [], article, child_titles, storage, proceeds

        else:
            pass

    elif type(article) is list:
        if len(article) == 0:
            proceed = {}
            proceed['child_titles'] = child_titles
            proceed['contents'] = contents
            proceeds.append(proceed)
            return article, [], child_titles, storage, proceeds
        else:
            for element in article:
                article, contents, child_titles, storage, proceeds = parse_children(
                    element, contents, child_titles, storage, proceeds
                )
            return article, contents, child_titles, storage, proceeds

    else:
        return [], contents.append(article), child_titles, storage, proceeds
