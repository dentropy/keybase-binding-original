import json
import pandas

with open("complexityweekend.json", "r") as read_file:
    print("Converting JSON encoded data into Python dictionary")
    data = json.load(read_file)
    packet = data['topic_name']['explore-KMS']['result']['messages']
    for p in packet:
        print("id: " + str(p['msg']['id']) + " | type: " + p['msg']['content']['type'] + " | user: " + p['msg']['sender']['username'])
    pandas.read_json(_,orient='records')