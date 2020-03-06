import copy
import random
from typing import List

import regex


class SectionTree:
    def __init__(self, titles, contents):
        self.titles: List[str] = titles
        self.contents: List[dict] = contents
        self.i = random.randint(0, 100)

    def __repr__(self):
        return "<SectionTree {} - {} - {}>".format(
            self.titles, self.contents, self.i)

    def to_dict(self):
        return {
            "titles": self.titles,
            "contents": self.contents
        }


class SectionParser:
    def __init__(self, current_titles: List[str] = [], current_level: int = 0):
        self.current_titles: List[str] = current_titles
        self.base_titles: List[str] = copy.copy(current_titles)
        self.header_contents: List[str] = []
        self.current_contents: List[str] = []
        self.section_trees: List[SectionTree] = []
        self.current_level: int = current_level

    def gather_tree(self, level: int):
        if len(self.current_contents) > 0:
            if (len(self.base_titles) != len(self.current_titles)):
                # current_contents => section_tree
                current_tree = SectionTree(
                    copy.copy(self.current_titles),
                    copy.copy(self.current_contents))
                self.section_trees.append(current_tree)

                self.current_contents = []
            else:
                # current_contents => header_contents
                self.header_contents = copy.copy(self.current_contents)
                self.current_contents = []
        if ((len(self.base_titles) != len(self.current_titles)) and
            (self.current_level >= level)):
            self.current_titles.pop(-1)
            if self.current_level > level:
                self.current_titles.pop(-1)

        self.current_level = level

    def __call__(self, articles: List = [], gather: bool = True):
        article_length = len(articles)
        idx = -1
        while True:
            if article_length <= idx + 1:
                break
            idx += 1
            article = articles[idx]

            if type(article) == str:
                self.current_contents.append(article)
            elif type(article) is dict:
                tag = article['tag']
                if (type(tag) is str and len(tag) == 2
                        and regex.match(r'h\d', tag)):
                    # subtitle is appeared
                    self.gather_tree(int(tag[1]))
                    self.current_titles.append(article['content'][0])
                else:
                    # a contents is appeared
                    section_trees, header_contents = SectionParser(
                        copy.copy(self.current_titles),
                        self.current_level)(article['content'])
                    article['content'] = []
                    article['content'] += header_contents

                    if len(article['content']) != 0:
                        self.current_contents.append(article)
                    if len(section_trees) != 0:
                        self.section_trees.append(section_trees)
        self.gather_tree(self.current_level)
        return self.section_trees, self.header_contents


def main():
    from service import contents_test
    y = SectionParser([])(copy.deepcopy(contents_test.testcase_3_data))
    print(y)
    return y


if __name__ == '__main__':
    main()
