# Export Team Keybase Chat to JSON

## Example bash commands

keybase chat help api
keybase chat -i getmessages.json

## Problems Solved

* Get messages sent to individual person
* Get messages from a teach channel
* Get list of team channels

## Get message from individual user

``` json
{
    "method": "get",
    "params": {
        "options": {
            "channel": {
                "name": "dentropy,docxology"
            },
            "message_ids": [1, 2, 3]
        }
    }
}
```

## Problems moving forward

* Topic Modeling on channels and across channels
* Graph number of people interacting in each channel
* Graph of where messages are distributed
* Generate a graph of activity over time
* Organize messages by most emojis
* Which users are most replied too
* Average message length by channel
* Total numbers of characters typed per user
* Total number of messages per use

## Library inspiration Stuff

* <https://github.com/keybase/pykeybasebot>
* <https://pypi.org/project/pykeybase/>
