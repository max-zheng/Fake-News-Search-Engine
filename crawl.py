from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import requests
import json

# Constants ------------------------------------------------------------------ #
sources = 'abc-news, ars-technica, associated-press, axios, bbc-news, bbc-sport, bleacher-report, bloomberg, breitbart-news, business-insider, business-insider-uk, buzzfeed, cbc-news, cbs-news, cnbc, cnn, crypto-coins-news, daily-mail, engadget, entertainment-weekly, espn, espn-cric-info, financial-post, financial-times, focus, fortune, four-four-two, fox-news, fox-sports, google-news, google-news-ca, google-news-uk, hacker-news, ign, independent, infobae, info-money, marca, mashable, medical-news-today, metro, mirror, msnbc, mtv-news, national-geographic, national-review, nbc-news, news24, new-scientist, newsweek, new-york-magazine, next-big-future, nfl-news, nhl0news, nrk, polygon, rbc, recode, reddit-r-all, reuters, rt, rte, spiegel-onllne, t3n, talksport, techcrunch, techradar, the-american-conservative, the-economist, the-globe-and-mail, the-guardian-uk, the-hill, the-huffington-post, the-lad-bible, the-new-york-times, the-next-web, the-sport-bible, the-telegraph, the-verge, the-wall-street-journal, the-washington-post, the-washingtom-times, time, usa-today, vice-news, wired, ynet'
parser_url = 'https://document-parser-api.lateral.io/'
key_location = 'api_keys.txt'
# ---------------------------------------------------------------------------- #

def getApiKeys():
    with open(key_location, 'r') as f:
        keys = f.read().split('\n')
        return keys

news_api_key, parser_api_key = getApiKeys()

newsapi = NewsApiClient(api_key=news_api_key)

# # /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(q='including lying to Congress and paying hush money to women who alleged affairs with',
#                                           sources='bbc-news,the-verge,abc-news,the-washington-times,usa-today,the-washington-post',
#                                           language='en')

# /v2/everything
all_articles = newsapi.get_everything(q='obama birth certificate',
                                      sources= sources,
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)

articles = all_articles['articles'][:20]

for article in articles:
    url = article['url']
    querystring = {'url':url}
    headers = {
        'subscription-key': parser_api_key,
        'content-type': 'application/json'
    }
    response = requests.get(parser_url, headers=headers, params=querystring)
    response_json = json.loads(response.text)
    if 'body' in response_json:
        print(response_json['body'])
