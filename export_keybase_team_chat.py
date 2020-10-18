from string import Template
import subprocess
import json

def get_team_channels(keybase_team_name):
    print("Executing `get_team_channels`: " + keybase_team_name)
    get_teams_channels = Template('''
    {
        "method": "listconvsonname",
        "params": {
            "options": {
                "topic_type": "CHAT",
                "members_type": "team",
                "name": "$TEAM_NAME"
            }
        }
    }
    ''')
    dentropydaemon_channels_json = get_teams_channels.substitute(TEAM_NAME=keybase_team_name)
    dentropydaemon_channels = subprocess.run(["keybase", "chat", "api", "-m", dentropydaemon_channels_json],  capture_output=True)
    dentropydaemon_channels = str(dentropydaemon_channels.stdout)[2:-3]
    mah_json = json.loads(dentropydaemon_channels)
    mah_channels = []
    for i in mah_json["result"]["conversations"]:
        mah_channels.append(i["channel"]["topic_name"])
    return mah_channels


def get_team_chat_channel(keybase_team_name, keybase_topic_name):
    print("Executing `get_team_chat_channel`: " + keybase_team_name + " & " + keybase_topic_name)
    get_teams_channels = Template('''
    {
        "method": "read",
        "params": {
            "options": {
                "channel": {
                    "name": "$TEAM_NAME",
                    "members_type": "team",
                    "topic_name": "$TOPIC_NAME"
                }
            }
        }
    }
    ''')
    dentropydaemon_channels_json = get_teams_channels.substitute(TEAM_NAME=keybase_team_name, TOPIC_NAME=keybase_topic_name)
    command = ["keybase", "chat", "api", "-m", dentropydaemon_channels_json]
    response = subprocess.check_output(command)
    return json.loads(response.decode('utf-8'))


def get_team_chat_channel_by_type(keybase_team_name, keybase_topic_name):
    print("Executing `get_team_chat_channels_by_type`: " + keybase_team_name + " & " + keybase_topic_name + " & text")
    tmp = Template('''
    {
        "method": "read",
        "params": {
            "options": {
                "channel": {
                    "name": "$TEAM_NAME",
                    "members_type": "team",
                    "topic_name": "$TOPIC_NAME"
                },
                "content": {
                    "type": "text"
                }
            }
        }
    }
    ''')
    dentropydaemon_channels_json = tmp.substitute(TEAM_NAME=keybase_team_name, TOPIC_NAME=keybase_topic_name)
    command = ["keybase", "chat", "api", "-m", dentropydaemon_channels_json]
    response = subprocess.check_output(command)
    return json.loads(response.decode('utf-8'))


complexity_weekend_teams = get_team_channels("complexweekend.oct2020")
mah_messages = {"topic_name":{}}
for topic in complexity_weekend_teams:
    mah_messages["topic_name"][topic] = get_team_chat_channel_by_type("complexweekend.oct2020", topic)

text_file = open("complexityweekend.json", "w")
print("Writing file...")
n = text_file.write(json.dumps(mah_messages))
print("complete!")
text_file.close()