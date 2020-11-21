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
def api_test_001(keybase_team_name, keybase_topic_name):
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
                        "num": 10
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

def api_test_002(keybase_team_name, keybase_topic_name, PAGIATION):
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
                    "num": 10
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
logs001 = api_test_001("dentropydaemon", "general")
logs002 = api_test_002("dentropydaemon", "general", logs001["result"]["pagination"]["next"])
```