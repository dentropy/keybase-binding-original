# snippits

## Just export some messages to an sql database

``` python
from create_export import ExportKeybase
ex_key = ExportKeybase()
ex_key.generate_json_export("dentropydaemon", "dentropydaemon.json")
ex_key.convert_json_to_sql("./dentropydaemon.json", "sqlite:///dentropydaemon.sqlite")
```

## Create an instance of the GenerateAnalytics class and get text all messages

``` python
from generate_analytics import GenerateAnalytics
gen = GenerateAnalytics("sqlite:///dentropydaemon.sqlite")
mah_messages = gen.get_all_team_messages("dentropydaemon")
print(mah_messages)
```

## Create an instance of the GenerateAnalytics class and get text all messages from a specific user

``` python
from generate_analytics import GenerateAnalytics
gen = GenerateAnalytics("sqlite:///dentropydaemon.sqlite")
mah_messages = gen.get_all_user_messages("dentropydaemon", "docxology")
print(mah_messages)
```

## Create an instance of the GenerateAnalytics class and get text all messages from a specific topic

``` python
from generate_analytics import GenerateAnalytics
gen = GenerateAnalytics("sqlite:///dentropydaemon.sqlite")
mah_messages = gen.get_all_topic_messages("dentropydaemon", "general")
print(mah_messages)
```
## keybase api pagination example

``` python
from string import Template
import subprocess
import json
def get_topic_messages_without_pagination(keybase_team_name, keybase_topic_name):
    get_teams_channels = Template('''{
        "method": "read",
            "params": {
                "options": {
                    "channel": {
                        "name": "$TEAM_NAME",
                        "members_type": "team",
                        "topic_name": "$TOPIC_NAME"
                    },
                    "pagination": {
                        "num": 100
                    }
                }
            }
        }
        ''')
    dentropydaemon_channels_json = get_teams_channels.substitute(
        TEAM_NAME=keybase_team_name, 
        TOPIC_NAME=keybase_topic_name
    )
    command = ["keybase", "chat", "api", "-m", dentropydaemon_channels_json]
    response = subprocess.check_output(command)
    return json.loads(response.decode('utf-8'))

def get_topic_messages_with_pagination(keybase_team_name, keybase_topic_name, PAGIATION):
    get_teams_channels = Template('''{
    "method": "read",
        "params": {
            "options": {
                "channel": {
                    "name": "$TEAM_NAME",
                    "members_type": "team",
                    "topic_name": "$TOPIC_NAME"
                },
                "pagination": {
                    "next": "$PAGIATION",
                    "num": 100
                }
            }
        }
    }
    ''')
    dentropydaemon_channels_json = get_teams_channels.substitute(
        TEAM_NAME=keybase_team_name, 
        TOPIC_NAME=keybase_topic_name,
        PAGIATION = PAGIATION
    )
    command = ["keybase", "chat", "api", "-m", dentropydaemon_channels_json]
    response = subprocess.check_output(command)
    return json.loads(response.decode('utf-8'))
# logs001 = get_topic_messages_without_pagination("dentropydaemon", "whatcha-up-to")
# logs002 = get_topic_messages_with_pagination("dentropydaemon", "whatcha-up-to", logs001["result"]["pagination"]["next"])
def get_all_topic_messages(team_name, topic_name):
    previous_query = get_topic_messages_without_pagination(team_name, topic_name)
    mah_messages = previous_query
    for i in range(int(previous_query["result"]["messages"][0]["msg"]["id"] / 10)):
        if "next" in previous_query["result"]["pagination"]:
            more_messages = get_topic_messages_with_pagination(team_name, topic_name, previous_query["result"]["pagination"]["next"])
            for message in more_messages["result"]["messages"]:
                mah_messages["result"]["messages"].append(message)
            previous_query = more_messages
    return mah_messages

test_messages = get_all_topic_messages("dentropydaemon", "general")
```