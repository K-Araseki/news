import sys
import time
from bs4 import BeautifulSoup
import pandas as pd
import requests

def soup(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')

    return soup

#各カテゴリのURL
topics = ['domestic','world','business','entertainment','sports','it','science','local']
base_url = 'https://news.yahoo.co.jp/topics/'

link_jump_dec = {}
#1ページ目から

for topic in topics:
    page=1
    link_jump_list=[]

    while 1:
        #1つのカテゴリ
        url = base_url + topic +'?page={}'.format(page)

        #続きを読むを押したあとのリンク

        if(soup(url).find('div',id = 'errorContents') == None):
            # 各記事のURLを取得し、そこからさらに続きを読むのリンクを取得してリストに追加
            for link in soup(url).find_all('a', class_='newsFeed_item_link'):
                soup_jump = soup(link.get('href'))
                link_jump = soup_jump.find('p', class_='sc-kaCJFH jSvclU')
                link_jump_list.append(link_jump.find('a').get('href'))
        else:
            print('ページが見つかりません')
            break
        print(page)
        time.sleep(1)
        page = page+1

    print(topic)
    #print(link_jump_list)
    link_jump_dec[topic] = link_jump_list

#print(link_jump_dec)


d = {'\u3000': None, '\n': None, ' ': None}
tbl = str.maketrans(d)
contents = []

#辞書のキーからトピック、リンクからタイトル・URL・記事を取得
for topic in topics:
    print('start')
    for url in link_jump_dec[topic]:

        soup_article = soup(url)

        title_tag = soup_article.find('h1',class_='sc-gVLVqr kEhnvA')
        if(title_tag == None):
            print('タイトルがありません')

        else:
            title = title_tag.text.translate(tbl)
            article = soup_article.find('p', class_='sc-kxynE cNCqYV yjSlinkDirectlink').text.translate(tbl)

            content = {'トピック': topic,
                       'タイトル': title,
                       'URL': url,
                       '記事': article}
            contents.append(content)
    time.sleep(1)

print(contents)


# 変数contentsを使って、データフレームを作成する
df = pd.DataFrame(contents)
df.to_csv('yahoo_info2021327.csv', index=None, encoding='utf-8-sig')
print(pd.read_csv('yahoo_info2021318.csv'))


"""title = soup_article.find('h1',class_='sc-gVLVqr kEhnvA').text
        #print(title)
        #sys.exit()
        article = soup_article.find('p',class_='sc-kxynE cNCqYV yjSlinkDirectlink').text
        content = {'トピック':topic,
                    'タイトル':title,
                    'URL':url,
                    '記事':article}
        contents.append(content)
        print(contents)"""

"""if soup_article.original_encoding == 'windows-1252':
    print('error')
    else:"""