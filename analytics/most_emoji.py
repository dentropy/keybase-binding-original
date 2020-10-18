import json
cw = json.load(open('/home/dentropy/Documents/Projects/pykeybasebot/json/complexityweekend.json', 'r'))
messages = {}
for topic_name in cw["topic_name"]:
    messages[topic_name] = {}
    for message_num in range(len(cw["topic_name"][topic_name]["result"]["messages"])):
        mah_msg = cw["topic_name"][topic_name]["result"]["messages"][message_num]["msg"]
        if mah_msg["content"]["type"] == "text":
            if mah_msg["id"] not in messages[topic_name]:
                messages[topic_name][mah_msg["id"]] = {"Reaction":[]}
            messages[topic_name][mah_msg["id"]]["text"] = mah_msg["content"]["text"]["body"]
        elif mah_msg["content"]["type"] == "reaction":
            root_msg = mah_msg["content"]["reaction"]["m"]
            if root_msg not in messages[topic_name]:
                messages[topic_name][root_msg] = {"Reaction":[]}
            Reaction_Object = {
                "id" : mah_msg["id"],
                "content" : mah_msg["content"]["reaction"]["b"]
            }
            messages[topic_name][root_msg]["Reaction"].append(Reaction_Object)

for topic in messages:
    for message_id in messages[topic]:
        if "Reaction" in messages[topic][message_id] and "text" in messages[topic][message_id]:
            print(messages[topic][message_id])
'''
* Topic Name
    * MSG ID
        * Text
        * Reaction ID
        * Reaction
'''
