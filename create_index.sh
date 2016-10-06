curl -XDELETE 'http://192.168.10.10:9200/qiita?pretty=true'
curl -XPUT 'http://192.168.10.10:9200/qiita?pretty=true' --data "@qiita_mapping.json"
curl -XPOST http://192.168.10.10:9200/usuao/_bulk?pretty=true --data-binary "@qiita.json";
