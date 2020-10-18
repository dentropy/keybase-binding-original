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

* Total number of characters typed per
  * User
  * Channel
* Total number of messages per
  * user
  * Channel
* Total number of users per
  * Topic
* Total number of people interacting in each channel
* Graph of activity over time
  * Total
  * Channel
  * User
  * User in Channel
* Most emojis per
  * Message
  * Channel, adjusted for total messages
* Which users are most replied too
* Average message length per
  * Channel
  * User
* Topic Modeling on channels and across channels

## Library inspiration Stuff

* <https://github.com/keybase/pykeybasebot>
* <https://pypi.org/project/pykeybase/>
