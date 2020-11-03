# Export Team Keybase Chat to JSON

## Installation

### Requirements

* [Anaconda data scince tool box](https://www.anaconda.com/products/individual)
  * Packages used include sqlalchemy, matplotlib, and a jupyter notebook
* Additional pip packages
  * URLExtract
  * tld
* [Keybase](https://keybase.io/download)

### Run the export tool

``` bash
pip3 install URLExtract
python3 create_export.py
```
If you want to change the keybase team, export json file, or sqlite json file you can do so in the last two lines of the create_export.py file

## Open the Jupyter Notebook

Navigate to this directory using the command line and run the following command,

``` bash
jupyter notebook
```

Your browser should open with a listing of the files associated with this project. Open generate_analyitics.py and have fun.


## GeneratedAnalyitcs Object

## DATA

* GeneratedAnalyitcs.user_list = []
* GeneratedAnalyitcs.topic_list = []
* GeneratedAnalyitcs.characters_per_user = {"user": [], "characters_per_user": []}
* GeneratedAnalyitcs.characters_per_topic = {"topic": [], "characters_per_topic": []}
* GeneratedAnalyitcs.messages_per_user = {"user": [], "messages_per_user": []}
* GeneratedAnalyitcs.messages_per_topic = {"topic": [], "messages_per_topic": []}
* GeneratedAnalyitcs.number_users_per_topic = {"users_list": [], "topics_list": []}
* GeneratedAnalyitcs.reaction_per_message  = {"ordered_mesage_id":[], "user_to_reaction":[]}
* GeneratedAnalyitcs.reaction_sent_per_user = {"ordered_user":[], "user_to_reaction":[]}
* GeneratedAnalyitcs.reaction_popularity_map = {"reactions":{}}
* GeneratedAnalyitcs.reactions_per_user = {"users_reactions":{}, "users_ordered":[]}
* GeneratedAnalytics.recieved_most_reactions = {"users_reactions":{}, "users_ordered":[]}
* GeneratedAnalytics.edits_per_user = {"users":{}, "ordered_users":[], "ordered_num_edits":[]}
* GeneratedAnalytics.edits_per_topic = {"topics":{}, "ordered_topics":[], "ordered_num_edits":[]}
* GeneratedAnalytics.deletes_per_user = {"users":{}, "ordered_users":[], "ordered_num_deletes":[]}
* GeneratedAnalytics.deletes_per_topic = {"topics":{}, "ordered_topics":[], "ordered_num_deletes":[]}
* GeneratedAnalytics.who_edits_most_per_capita = {"users":{}, "ordered_users":[], "ordered_edit_per_capita" : []}
* GeneratedAnalytics.top_domains = {"URLs":{}, "top_domains_sorted":[], "num_times_repeated":[]}
## Methods

* GeneratedAnalyitcs.get_message(MESSAGE_ID_NUM)
* GeneratedAnalyitcs.get_num_messages_from_user("USERS USERNAME") = {"edit": INT, "text": INT, "delete": INT}
* GeneratedAnalyitcs.get_reaction_poplarity_topic("TOPIC NAME") = {"reactions":{}, "list":[]}
* GeneratedAnalyitcs.get_all_user_message_id("USERS USERNAME") = {"users_reactions":{}, "users_ordered":[]}
* GeneratedAnalyitcs.get_reaction_type_popularity_per_user("USERS USERNAME") = {"users_reactions":{}, "reactions_ordered":[]}

## TODO

## Analitics

* Finish the last couple methods in generate_analytics and then output their data in one or both of the jupyter notebooks
* Script to Export all attachments, must use keybase daemon
* Hook up the database to graphql
* Generate as many graphs as resonable using generate_graphs.ipynb

## Implimentaion Details

* Not importing Pin Message type because unable to find refence to message being pinned
* Not importing additional metadata such as device ID , device name, reactions within a message, and team_mentions though we may want to
* Wherever json.dumps is used in create_export it may not be desireable

## Problems moving forward

* Total number of characters per
  * User
  * Channel
* Total number of messages per
  * user
  * Channel
* Total number of words per
  * User
  * Channel
  * Message per Topic
* Total number of users per
  * Topic
* Most Reactions per
  * Message
  * User
* Total number of people interacting in each channel
----- Above is completed
* reaction_poplarity_per_topic
* user_sent_most_reactions
* user_recieved_most_reactions
* reaction_type_popularity_per_user
* Graph of activity over time
  * Total
  * Channel
  * User
  * User in Channel
* Which users are most replied too
* Average message length per
  * Channel
  * User
* Topic Modeling on channels and across channels
* Sentiment Analysis

## Tools moving forward

<https://www.nltk.org/>

## Library inspiration Stuff

* <https://github.com/keybase/pykeybasebot>
* <https://pypi.org/project/pykeybase/>
