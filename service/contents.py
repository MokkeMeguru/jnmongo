from typing import List, Dict, Union
import regex
import random
import copy
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
        return "<SectionTree {} - {} - {}>".format(self.titles, self.contents, self.i)


class SectionParser:
    def __init__(self, current_titles: List[str] = []):
        self.current_titles: List[str] = current_titles
        self.current_contents: List[str] = []
        self.section_trees: List[SectionTree] = []

    def gather_tree(self):
        if len(self.current_contents) != 0:
            print('currents', self.current_titles)
            print('>>', self.current_contents)
            print('>> currents trees', self.section_trees)
            current_tree = SectionTree(
                copy.copy(self.current_titles), copy.copy(self.current_contents))
            self.section_trees += [current_tree]
            print('updated trees', self.section_trees)
            self.current_contents = []

    def __call__(self, articles: List = [], gather: bool=True):
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
                if (type(tag) is str
                    and len(tag) == 2
                    and regex.match(r'h\d', tag)):
                    self.gather_tree()
                    self.current_titles.append(article['content'][0])
                else:
                    section_trees, rest_article = SectionParser(
                        self.current_titles)(article['content'], False)
                    print('rest', rest_article)
                    print('tree', section_trees)
                    article['content'] = rest_article
                    
                    if len(article) != 0:
                        self.current_contents.append(article)
                    if len(section_trees) != 0:
                        self.section_trees.append(section_trees)

        if gather:
            self.gather_tree()
            return self.section_trees
        else:
            return self.section_trees, self.current_contents

def main():
    import contents_test
    y = SectionParser([])(copy.deepcopy(contents_test.testcase_3_data))
    print(y)
    return y

if __name__ == '__main__':
    main()



    # def __call__(self, articles: Union[List, Dict, str]):
    #     if type(articles) is None or len(articles) == 0:
    #         return self.current_contents, self.section_trees
    #     if type(articles) == str:
    #         self.current_contents.append(articles)
    #         return self.current_contents, self.section_trees
    #     if type(articles) == dict:
    #         tag = articles['tag']
    #         if regex.match(r'h\d', tag) and len(tag) == 2:
    #             self.current_titles.append(articles['content'][0])
    #             contents, section_trees = SectionParser(
    #                 self.current_titles)(articles['content'][1:])
    #             self.section_trees += section_trees
    #             self.current_contents += contents
    #         else:
    #             current_contents, section_trees = SectionParser(
    #                 self.current_titles)(articles['contents'])
    #             articles['contents'] = current_contents
    #             self.current_contents.append(articles)
    #             if len(section_trees) > 0:
    #                 self.section_trees.append(section_trees)
    #             return self.current_contents, self.section_trees
    #     if type(articles) == list:
    #         for article in articles:
    #             tag = article['tag']
    #             if regex.match(r'h\d', tag) and len(tag) == 2:
    #                 self.current_titles.append(article['content'][0])
    #                 contents, section_trees = SectionParser(
    #                     self.current_titles)(article['content'][1:])
    #                 self.section_trees += section_trees
    #                 self.current_contents += contents
    #             else:
    #                 # TODO: recursive search
    #                 # 1. hold section
    #                 # 2. unhold section
    #                 contents, section_trees = SectionParser(
    #                     self.content_titles)(article[0]['content'])
    #                 self.current_contents.append(contents)
    #                 self.section_trees.append(section_trees)
    #             return self.current_contents, self.section_trees
