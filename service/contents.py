import copy
import random
from typing import Dict, List, Union

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


class SectionTree:
    def __init__(self, titles, contents):
        self.titles: List[str] = titles
        self.contents: List[dict] = contents
        self.i = random.randint(0, 100)

    def __repr__(self):
        return "<SectionTree {} - {} - {}>".format(
            self.titles, self.contents, self.i)


class SectionParser:
    def __init__(self, current_titles: List[str] = []):
        self.current_titles: List[str] = current_titles
        self.base_titles: List[str] = copy.copy(current_titles)
        self.header_contents: List[str] = []
        self.current_contents: List[str] = []
        self.section_trees: List[SectionTree] = []

    def gather_tree(self):
        if len(self.current_contents) > 0:
            print(self.base_titles, "vs", self.current_titles)
            if (len(self.base_titles) != len(self.current_titles)):
                # current_contents => section_tree
                print('currents', self.current_titles)
                print('>>', self.current_contents)
                print('>> currents trees', self.section_trees)
                current_tree = SectionTree(
                    copy.copy(self.current_titles),
                    copy.copy(self.current_contents))
                self.section_trees.append(current_tree)
                print('updated trees', self.section_trees)
                self.current_contents = []
            else:
                # current_contents => header_contents
                print('currents title', self.current_titles)
                self.header_contents = copy.copy(self.current_contents)
                print('updated header', self.header_contents)
                self.current_contents = []

    def __call__(self, articles: List = [], gather: bool = True):
        article_length = len(articles)
        idx = -1
        while True:
            if article_length <= idx + 1:
                break
            idx += 1
            article = articles[idx]
            print('art', idx,  article)

            if type(article) == str:
                self.current_contents.append(article)
            elif type(article) is dict:
                tag = article['tag']
                if (type(tag) is str and len(tag) == 2
                        and regex.match(r'h\d', tag)):
                    # subtitle is appeared
                    self.gather_tree()
                    self.current_titles.append(article['content'][0])
                else:
                    # a contents is appeared
                    print('content', article['content'])
                    section_trees, header_contents = SectionParser(
                        copy.copy(self.current_titles))(article['content'])
                    print('header', header_contents)
                    print('tree', section_trees)
                    print('append to', article['tag'],
                          header_contents)
                    article['content'] = []
                    article['content'] += header_contents

                    if len(article['content']) != 0:
                        self.current_contents.append(article)
                    if len(section_trees) != 0:
                        self.section_trees.append(section_trees)
        self.gather_tree()
        return self.section_trees, self.header_contents
      

def main():
    from service import contents_test
    y = SectionParser([])(copy.deepcopy(contents_test.testcase_3_data))
    print(y)
    return y


if __name__ == '__main__':
    main()
