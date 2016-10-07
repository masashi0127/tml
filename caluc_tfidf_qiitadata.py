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

def get_doc_count():
    es = Elasticsearch([
        {'host': '192.168.10.10'}
    ])

    retval = es.count(index='qiita', doc_type='news')
    return retval['count']

def get_qiita_news(c):
    es = Elasticsearch([
        {'host': '192.168.10.10'}
    ])

    body = {
        "size": c,
        "query": {
            "match_all": {}
        }
    }

    retdata = es.search(index='qiita', doc_type='news', body=body)

    docs = []
    doc = []

    for r in retdata['hits']['hits']:
        d = r['_source']
        res = es.indices.analyze(index='qiita', analyzer='simple_analyzer', text=d['title'])
        docs.append(' '.join([t['token'] for t in res['tokens']]))
    return docs

def tfidf(docs):
    vectorizer = TfidfVectorizer(min_df=1, max_df=50, token_pattern=u'(?u)\\b\\w+\\b')
    features = vectorizer.fit_transform(docs)
    terms = vectorizer.get_feature_names()

    return features, terms

def ranking(terms, features_array):
    rank = {}
    for fa in features_array:
        for i, f in enumerate(fa):
            if f > 0:
                rank[terms[i]] = f
    return [t for t, _ in sorted(rank.items(), key=lambda x:x[1], reverse=True)]

def main():
    c = get_doc_count()
    docs = get_qiita_news(c)
    features, terms = tfidf(docs)
    rank = ranking(terms, features.toarray())
    pprint(rank[:100])

if __name__ == '__main__':
    main()
