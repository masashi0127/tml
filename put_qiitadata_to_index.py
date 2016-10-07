# conding: utf-8;
import pycurl
import json
import os
from io import BytesIO
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch import helpers as Ehelpers

def get_header():
    token = os.environ['QIITA_TOKEN']
    header = [
        'Authorization: Bearer ' + token
    ]

    url = 'http://qiita.com/api/v2/items?per_page=100&query=created:>2014-01-01+created<2016-12-31'
    buffer = BytesIO()

    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, header)
    curl.setopt(pycurl.HEADER, 1)
    curl.setopt(pycurl.NOBODY, 1)
    curl.setopt(curl.HEADERFUNCTION, buffer.write)

    try:
        curl.perform()
        http_code = curl.getinfo(pycurl.HTTP_CODE)

        if http_code == 200:
            retval = buffer.getvalue()
        else:
            retval = str(http_code)
    except Exception as e:
        retval = str(e)

    print(retval)
    return True

def register_contents():
    token = os.environ['QIITA_TOKEN']
    header = [
        'Content-Type: application/json',
        'Authorization: Bearer ' + token
    ]
    for i in range(1, 100):
        url = 'http://qiita.com/api/v2/items?page=' + str(i) + '&per_page=100&query=created:>2014-01-01+created<2016-12-31'
        buffer = BytesIO()

        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.HTTPHEADER, header)
        curl.setopt(curl.WRITEDATA, buffer)
        curl.perform()
        body = buffer.getvalue()
        data = json.loads(body.decode('utf-8'))

        docs = []
        
        for d in data:
            docs.append({
                '_op_type': 'create',
                '_index': 'qiita',
                '_type': 'news',
                '_source': {
                    'id': d['id'],
                    'title': d['title'],
                    'created_at': d['created_at'][:10]
                }
            })

        es = Elasticsearch([
            {'host': '192.168.10.10'}
        ])
        Ehelpers.bulk(es, docs)

def main():
    # get_header()
    register_contents()

if __name__ == '__main__':
    main()
