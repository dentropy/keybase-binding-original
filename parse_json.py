import json
import pandas as pd

def char_len(s):
    count = 0
    for c in s:
        count = count + 1
    return count

def parse_recipient(msg):
    try:
        recipient = msg["at_mention_usernames"]
    except:
        recipient = ""
    return recipient

    # keys = msg.keys
    # recipient = ""
    # for k in keys:
    #     if k == "at_mention_usernames":
    #         recipient = msg[k]
    # return recipient


def word_len(s):
    count = 1
    for c in s:
        if c.isspace():
            count = count + 1
    return count



with open("complexityweekend.json", "r") as read_file:
    print("Converting JSON encoded data into Python dictionary")
    data = json.load(read_file)
    x = []

    for topic in data['topic_name']:
        packet = data['topic_name'][topic]['result']['messages']
        for p in packet:
            print("id: " + str(p['msg']['id']) + " | type: " + p['msg']['content']['type'] + " | user: " + p['msg']['sender']['username'])
            if (p['msg']['content']['type']=="text"):
                x.append({'id': p['msg']['conversation_id'] + "-" + str(p['msg']['id']),
                          'topic': topic,
                          'type': 'text',
                          'time': str(p['msg']['sent_at']),
                          'message': p['msg']['content']['text']['body'],
                          'nChar': char_len(p['msg']['content']['text']['body']),
                          'nWord': word_len(p['msg']['content']['text']['body']),
                          'channelMention': p['msg']['channel_mention'],
                          'userMentions': p['msg']['content']['text']['userMentions'],
                          'teamMentions': p['msg']['content']['text']['teamMentions'],
                          'emojis': p['msg']['content']['text']['emojis'],
                          'sender': p['msg']['sender']['username'],
                          'recipient': parse_recipient(p['msg'])})
            elif (p['msg']['content']['type']=="reaction"):
                x.append({'id': p['msg']['conversation_id'] + "-" + str(p['msg']['content']['reaction']['m']),
                          'topic': topic, 
                          'type': 'reaction',
                          'time': str(p['msg']['sent_at']),
                          'message': "",
                          'nChar': 0,
                          'nWord': 0,
                          'channelMention': "",
                          'userMentions': "",
                          'teamMentions': "",
                          'emojis': p['msg']['content']['reaction']['b'],
                          'sender': p['msg']['sender']['username'],
                          'recipient': parse_recipient(p['msg'])})

        out = pd.DataFrame.from_dict(x, orient='columns')
        print(out)

with pd.ExcelWriter('complexityweekend_text.xlsx') as writer:
    print('Saving spreadsheet...')
    out.to_excel(writer)
    print('complete!')
