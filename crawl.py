from newsapi import NewsApiClient
from operator import itemgetter
import requests
import json
import nltk

# Constants ------------------------------------------------------------------ #
sources = 'abc-news, ars-technica, associated-press, axios, bbc-news, bbc-sport, bleacher-report, bloomberg, breitbart-news, business-insider, business-insider-uk, buzzfeed, cbc-news, cbs-news, cnbc, cnn, crypto-coins-news, daily-mail, engadget, entertainment-weekly, espn, espn-cric-info, financial-post, financial-times, focus, fortune, four-four-two, fox-news, fox-sports, google-news, google-news-ca, google-news-uk, hacker-news, ign, independent, infobae, info-money, marca, mashable, medical-news-today, metro, mirror, msnbc, mtv-news, national-geographic, national-review, nbc-news, news24, new-scientist, newsweek, new-york-magazine, next-big-future, nfl-news, nhl0news, nrk, polygon, rbc, recode, reddit-r-all, reuters, rt, rte, spiegel-onllne, t3n, talksport, techcrunch, techradar, the-american-conservative, the-economist, the-globe-and-mail, the-guardian-uk, the-hill, the-huffington-post, the-lad-bible, the-new-york-times, the-next-web, the-sport-bible, the-telegraph, the-verge, the-wall-street-journal, the-washington-post, the-washingtom-times, time, usa-today, vice-news, wired, ynet'
parser_url = 'https://document-parser-api.lateral.io/'
key_location = 'api_keys.txt'
query = 'obama birth certificate'

# Functions ------------------------------------------------------------------ #
def getApiKeys():
    with open(key_location, 'r') as f:
        keys = f.read().split('\n')
        return keys

def getArticles():
    result = {}
    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q=query,
                                              sources='bbc-news,the-verge,abc-news,the-washington-times,usa-today,the-washington-post',
                                              language='en')
    all_headlines = newsapi.get_everything(q=query, sources= sources, language='en',
                                sort_by='relevancy', page=1)
    result.update(top_headlines)
    result.update(all_headlines)
    return result

def parseArticles(articles):
    parsed_articles = {}
    for article in articles:
        url = article['url']
        querystring = {'url':url}
        headers = {
            'subscription-key': parser_api_key,
            'content-type': 'application/json'
        }
        response = requests.get(parser_url, headers=headers, params=querystring)
        response_json = json.loads(response.text)
        if 'body' in response_json and 'title' in response_json:
            parsed_articles[response_json['title']] = response_json['body']

    return parsed_articles

def splitQueryBigrams():
    tokens = nltk.word_tokenize(query)
    bigram_tuple = list(nltk.bigrams(tokens))
    bigram = []
    for tuple in bigram_tuple:
        bigram.append(tuple[0] + ' ' + tuple[1])
    return bigram

def countOccurences(bigram_query, parsed_articles):
    # which paragraphs in each document have a bigram match
    paragraph_map = {}
    # how many bigram matches for each document
    occurence_map = {}

    for key in parsed_articles:
        match_score = 0
        article_text = parsed_articles[key]
        bigram_set = set()

        article_paragraphs = article_text.split('\n\n')
        for p in range(0, len(article_paragraphs)):
            paragraph = article_paragraphs[p]

            for i in range(0,len(paragraph)):
                for bigram in bigram_query:
                    if i + len(bigram) >= len(paragraph):
                        continue

                    if paragraph[i:i + len(bigram)].lower() == bigram.lower():
                        match_score += 1
                        addToParagraphMap(paragraph_map, key, p)
                        bigram_set.add(bigram.lower())

        # heavy weight for each unique bigram
        match_score += 50 * len(bigram_set)
        occurence_map[key] = match_score

    return occurence_map, paragraph_map

def addToParagraphMap(paragraph_map, key, p):
    if not key in paragraph_map:
        paragraph_map[key] = set()

    paragraph_map[key].add(p)

def sortMap(occurence_map):
    return sorted(occurence_map.items(), key=itemgetter(1), reverse=True)

def displayRelevantParagraphs(parsed_articles, sorted_map, paragraph_map):
    for (key, value) in sorted_map:
        if key in paragraph_map:
            paragraph_list = list(paragraph_map[key])
            article_text = parsed_articles[key]
            article_paragraphs = article_text.split('\n\n')
            print('--{}--'.format(key))
            for p in paragraph_list:
                print(article_paragraphs[p])
            print('')

# Execute -------------------------------------------------------------------- #
news_api_key, parser_api_key = getApiKeys()
newsapi = NewsApiClient(api_key=news_api_key)
articles = getArticles()

articles = articles['articles']
parsed_articles = parseArticles(articles)
bigram_query = splitQueryBigrams()

occurence_map, paragraph_map = countOccurences(bigram_query, parsed_articles)
sorted_map = sortMap(occurence_map)

displayRelevantParagraphs(parsed_articles, sorted_map, paragraph_map)
