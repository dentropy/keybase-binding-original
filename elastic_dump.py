import json
import urllib3
from elasticsearch import Elasticsearch
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

my_index = "test001"
es = Elasticsearch(
  ['https://elastic:rgIcWCIg2IMNmnoRIJMudHEXVVFyPk5@elasticsearch.dentropy.local:443'],
  verify_certs=False)
try:
  es.indices.create(index=my_index)
except:
  print("Index already created")
es.indices.put_settings(index=my_index, body={
    "index.mapping.total_fields.limit": 2000
})

import json
index_count = 1
with open('./exports/dentropydaemon-messages.json') as json_file:
    data = json.load(json_file)
for topic in data["topic_name"]:
    for message_num in range(len(data["topic_name"][topic]["result"]["messages"])):
        #print(data["topic_name"][topic]["result"]["messages"][message_num])
        try:
            res = es.index(index=my_index, id=index_count, body=data["topic_name"][topic]["result"]["messages"][message_num])
            index_count += 1
            print(res['result'], index_count)
        except Exception as e: 
            print(e)
            with open("error.json", "a") as my_file:
                my_file.write("\n")
                my_file.write(json.dumps(data["topic_name"][topic]["result"]["messages"][message_num]))
          