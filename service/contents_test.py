# FAILED
testcase_1_data = [
    {'tag': 'h2',
     'content': ['title1']},
    {'tag': None,
     'content': ['hy!']},
    {'tag': 'h3',
     'content': ['title2']},
    {'tag': None,
     'content': [
         {'tag': None,
          'content': ['hello']}]}]

testcast_1_answer = [
    {'titles': ['title1'],
     'contents': [
         {'tag': None,
          'content': ['hy!']}]},
    {'titles': ['title1', 'title2'],
     'contents': [
         {'tag': None,
          'content': [
              {'tag': None,
               'conent': ['hello']}]}]}]

# FAILED
testcase_2_data = [
    {'tag': 'h2',
     'content': ['title1']},
    {'tag': None,
     'content': ['hy!']},
    "hi",
    {'tag': 'h3',
     'content': ['title2']},
    {'tag': None,
     'content': [
         {'tag': None,
          'content': ['hello']}]}]

testcast_2_answer = [
    {'titles': ['title1'],
     'contents': [
         {'tag': None,
          'content': ['hy!']}]},
    {'titles': ['title1', 'title2'],
     'contents': [
         {'tag': None,
          'content': [
              {'tag': None,
               'conent': ['hello']}]}]}]


# FAILED
testcase_2_data = [
    {'tag': 'h2',
     'content': ['title1']},
    {'tag': None,
     'content': [
         {'tag': None,
          'content': ['hy!']},
         {'tag': 'h3',
          'content': ['title2']},
         {'tag': None,
          'content': [
              {'tag': None,
               'content': ['hello']}]}]}]

testcast_2_answer = [
    {'titles': ['title1'],
     'contents': [{'tag': None,
                   'content': [
                       {'tag': None,
                        'content': ['hy!']}]}]},
    {'titles': ['title1', 'title2'],
     'contents': [
         {'tag': None,
          'content': [
              {'tag': None,
               'conent': ['hello']}]}]}]

if __name__ == '__main__':
    from . import contents
    print(contents.SectionParser([], testcase_1_data)())
