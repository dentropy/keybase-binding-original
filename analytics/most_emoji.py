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

message_to_reaction = {}
for topic in messages:
    for message_id in messages[topic]:
        if messages[topic][message_id]["Reaction"] != [] and "text" in messages[topic][message_id]:
            #print(len(messages[topic][message_id]["Reaction"]))
            message_to_reaction[str(topic + "," + str(message_id))] = len(messages[topic][message_id]["Reaction"])
            #print(messages[topic][message_id])

sort_orders = sorted(message_to_reaction.items(), key=lambda x: x[1], reverse=True)

for i in sort_orders:
    print(i[0], i[1])
    ummm_IDK = i[0].split(",")
    print(messages[ummm_IDK[0]][int(ummm_IDK[1])])

'''
* Topic Name
    * MSG ID
        * Text
        * Reaction
'''
