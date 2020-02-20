# PASS
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

# PASS
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
testcase_3_data = [
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

testcast_3_answer = [
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
