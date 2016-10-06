# conding: utf-8;
from scipy import sparse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pycurl
import json
import os
from io import BytesIO
from elasticsearch import Elasticsearch
from pprint import pprint

def tfidf(docs):
    vectorizer = TfidfVectorizer(min_df=1, max_df=50, token_pattern=u'(?u)\\b\\w+\\b')
    features = vectorizer.fit_transform(docs)
    terms = vectorizer.get_feature_names()

    return features, terms

def get_qiita_news():
    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, 'http://qiita.com/api/v2/items?page=1&per_page=100')
    curl.setopt(curl.WRITEDATA, buffer)
    curl.perform()
    body = buffer.getvalue()
    data = json.loads(body.decode('utf-8'))

    if os.path.isfile('qiita.json'):
        os.remove('qiita.json')

    fout = open('qiita.json', 'wt')

    es = Elasticsearch([
        {'host': '192.168.10.10'}
    ])

    docs = []
    doc = []
    for d in data:
        res = es.indices.analyze(index='qiita', analyzer='simple_analyzer', text=d['title'])
        docs.append(' '.join([t['token'] for t in res['tokens']]))
    return docs

def ranking(terms, features_array):
    rank = {}
    for fa in features_array:
        for i, f in enumerate(fa):
            if f > 0:
                rank[terms[i]] = f
    return [t for t, _ in sorted(rank.items(), key=lambda x:x[1], reverse=True)]

def main():
    docs = get_qiita_news()

    features, terms = tfidf(docs)

    rank = ranking(terms, features.toarray())

    pprint(rank)

if __name__ == '__main__':
    main()
