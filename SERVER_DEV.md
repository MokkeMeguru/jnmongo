# SERVER DEVELOPMENT DOCUMENT

## SERVER APP
[app.py](app.py)

## endpoints

- /list: GET    
    保存しているドキュメントのリストを得る

    Returns:
    ```
    {
        body :
          [
            "title_1",
            "title_2",
            ...
          ]
    }
    ```

    Example:
    ```
    curl http://localhost:8085/list | jq .

    {
      "Content-Type": "application/json",
      "body": [
        "鈴原るる",
        "カニ",
        "コアラ",
        "キツネ",
        "エビ",
        "三枝明那",
        "イルカ",
        "でびでび・でびる",
        "馬",
        "エクス・アルビオ"
      ]
    }
    ```
- /related_words: GET    
    ドキュメントの関連用語を得る
    
    Args:
    - doc_title (string): ドキュメントのタイトル ref. /list
    Returns:
    ```
    {
    "Content-Type": "application/json",
      "body": [
        "甲殻類",
        "ヤドカリ",
        "不動遊星",
        "暴力二男",
        "ニコニコ水族館",
        "カニ頭",
        "蟹光線/カニ光線",
        "ぐんたいガニ",
        "動物の一覧",
        "エビ",
        "キングラー/クラブ(ポケモン)",
        "蟹になりたい"
      ]
    }
    ```

- /contents: GET    
    ドキュメントのコンテンツ部分を得る
    
    Args:
    - doc_title (string): ドキュメントのコンテンツ部分
    
    Returns:
    ```
    {
    "Content-Type": "application/json",
    "body": [
      {
        "candidates": [],
        "child_titles": [
          "カニの一覧"
        ],
        "contents": [
          {
            "attrs": null,
            "content": [
              {
                "attrs": null,
                "content": [
                  "アカガニ"
                ],
                "tag": "li",
                "type": "element"
              },
              {
                "attrs": null,
                "content": [
                  "アカテガニ"
                ],
                "tag": "li",
                "type": "element"
              },
              {
                "attrs": null,
                "content": [
                  "ミナミスナガニ"
                ],
                "tag": "li",
                "type": "element"
              }
            ],
            "tag": "ul",
            "type": "element"
          }
        ]
      },
      {
        "candidates": [],
        "child_titles": [
          "関連項目"
        ],
        "contents": [
          {
            "attrs": null,
            "content": [
              {
                "attrs": null,
                "content": [
                  "動物の一覧"
                ],
                "tag": "li",
                "type": "element"
              },
              {
                "attrs": null,
                "content": [
                  "エビ"
                ],
                "tag": "li",
                "type": "element"
              },
              {
                "attrs": null,
                "content": [
                  "蟹光線/カニ光線"
                ],
                "tag": "li",
                "type": "element"
              }
            ],
            "tag": "ul",
            "type": "element"
          }
        ]
        }
      ]
    }
    ```
    Notes:    
    コンテンツ...記事内のセクション。セクションは h タグで区切られているものとみなす。
