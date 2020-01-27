
# Table of Contents

1.  [keyword](#org9fc3efc)
2.  [content](#orgab67600)
3.  [abst](#org452d942)
4.  [related words](#orgb42ac82)

DB設計


<a id="org9fc3efc"></a>

# keyword

    {
      keyword: str
    }

-   keyword
    タイトルや用語(主に名詞句)


<a id="orgab67600"></a>

# content

    { 
      doc_title: object_id->keywords,
      child_titles: array,
      contents: json
    }

-   doc \_ title
    keyword の object<sub>id</sub>
-   child \_ titles
    ["概要"] や ["概要" "プロフィール"] のようなセクション名のリスト
-   contents
    jsonize された HTML データ


<a id="org452d942"></a>

# abst

    {
      doc_title: object_id->keywords,
      content: json
    }

-   doc \_ title
    keyword の object \_ id
-   content
    jsonize された HTML データ


<a id="orgb42ac82"></a>

# related words

    {
      doc_title: object_id->keywords,
      texts: array,
      contents: json
    }

-   doc \_ title
    keyword の object \_ id
-   texts
    contents からテキストのみを抽出したリスト
-   contents
    jsonize された HTML データ

