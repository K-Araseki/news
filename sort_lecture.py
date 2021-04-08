import MeCab
import pandas as pd

df = pd.read_csv('yahoo_info2021318.csv').values.tolist()
topics = []
articles = []

#サンプル用に10個のデータ（分類と記事）を抽出
for content in df:
    topics.append(content[0])
    articles.append(content[3])
    if len(topics) >= 10:
        break

#全ての記事を表
print(articles)

"""article = articles[0]
print(article)"""

import mojimoji
import re
def replace_text(text):
    text.lower()
    return mojimoji.han_to_zen(text)

def normalize_number(text):
    # 連続した数字を0で置換
    replaced_text = re.sub(r'\d+', '0', text)
    return replaced_text

#形態素解析（記事ごとに行う）関数にしてもいいかも
mecab = MeCab.Tagger('-Ochasen')
article_datas = []

for article in articles:
    article_data = []
    node = mecab.parseToNode(article)

    #名詞だけをリストに追加する
    while node:
        if node.feature.split(',')[0] == '名詞':
            text = node.surface
            text = replace_text(text)
            text = normalize_number(text)
            article_data.append(text)
        node = node.next

    article_datas.append(article_data)


#名詞のみのリストを表示
print(article_datas)


