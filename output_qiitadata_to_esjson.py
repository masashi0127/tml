# conding: utf-8;
import pycurl
import json
import os
from io import BytesIO
from pprint import pprint


def main():
    buffer = BytesIO()
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, 'http://qiita.com/api/v2/items?page=1&per_page=20')
    curl.setopt(curl.WRITEDATA, buffer)
    curl.perform()
    body = buffer.getvalue()
    data = json.loads(body.decode('utf-8'))

    if os.path.isfile('qiita.json'):
        os.remove('qiita.json')

    fout = open('qiita.json', 'wt')

    for d in data:
        print('{"index": {"_index": "qiita", "_type": "news"}}', file=fout)
        print('{{"id": "{}", "title": "{}"}}'.format(d['id'], d['title']), file=fout)

if __name__ == '__main__':
    main()
