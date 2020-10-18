import json
cw = json.load(open('/home/dentropy/Documents/Projects/pykeybasebot/json/complexityweekend.json', 'r'))
user_character_count = {}
for topic_name in cw["topic_name"]:
    for message_num in range(len(cw["topic_name"][topic_name]["result"]["messages"])):
        if cw["topic_name"][topic_name]["result"]["messages"][message_num] != None:
            tmp_msg = (cw["topic_name"][topic_name]["result"]["messages"][message_num]["msg"])
            if (tmp_msg["content"]["type"]) == "text":
                username = tmp_msg["sender"]["username"]
                msg_text = tmp_msg["content"]["text"]["body"]
                if username in user_character_count:
                    user_character_count[username] += len(msg_text)
                else:
                    user_character_count[username] = len(msg_text)
print(user_character_count)

sort_orders = sorted(user_character_count.items(), key=lambda x: x[1], reverse=True)

for i in sort_orders:
	print(i[0], i[1])