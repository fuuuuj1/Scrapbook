import requests
import json
import feedparser

from datetime import datetime
# from constants import RSS_FEEDS

class Article:
    def __init__(self, json):
        self.title = json['title']
        self.link = json['link']
        self.description = json['description']
    
    def to_dict(self):
        return {
            'title': self.title,
            'link': self.link,
            'description': self.description
        }

# main function
def handler():
    # batch実行日時から日付 + AM/PMを取得する
    date = datetime.now().strftime('%Y-%m-%d-%p')

    # articles の key にはサイト名、value には記事のリストが入る
    articles = {}

    # TODO: 別ファイルに定義したRSS_FEEDSを使う 
    urls = {
        "qiita" : "https://qiita.com/popular-items/feed.atom",
        "zenn" : "https://zenn.dev/feed",
        "hatena": "https://b.hatena.ne.jp/hotentry/it.rss",
    }

    for key, url in urls.items():
        articles[key] = fetch(url)

    # Generate a json file
    file = generate_json(articles, date)
    
    return file

# Fetch the articles from the url
def fetch(url) -> dict:
    try:
        feeds = feedparser.parse(url).entries

        articles = []

        # 10件まで取得する
        for feed in feeds[:10]:
            # 事前に定義したArticleクラスを使ってインスタンスを生成する
            article = Article(feed)
            articles.append(article.to_dict())
        return articles

    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
    except ValueError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return []

# create a json file
def generate_json(articles, date) -> str:
    file = f'{date}.json'
    with open(file, 'w') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    return file

if __name__ == '__main__':
    result = handler()
    print(result)
