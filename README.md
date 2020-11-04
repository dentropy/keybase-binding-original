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
python3 create_export_example.py
```
If you want to change the keybase team, export json file, or sqlite json file you can do so in the last two lines of the create_export.py file

## Open the Jupyter Notebook

Navigate to this directory using the command line and run the following command,

``` bash
jupyter notebook
```

Your browser should open with a listing of the files associated with this project. Open generate_analyitics.py and have fun.


## ExportKeybase Class

* ExportKeybase.get_teams()
  * Returns string list of teams current loggedin keybase user belongs to
* ExportKeybase.get_team_memberships(team_name)
  * Returns string list of usernames on that team
* ExportKeybase.get_user_metadata(username)
  * Get string of URLs where user has verified their keybase identity plus all teams they are on
* ExportKeybase.export_team_user_metadata()
  * Write a json file of all users, where they are verified and what teams they are on
  * **Should probably just return an object rather than writing to disk**
* ExportKeybase.get_team_channels(keybase_team_name)
  * Returns list of strings for each text channel on a team
* ExportKeybase.get_team_chat_channel(keybase_team_name, keybase_topic_name)
  * Returns object of all messages within a keybase team topic
* ExportKeybase.generate_json_export(keybase_team, output_file)
  * Creates a json file named output_file which contains all chat messages from an antire team
  * **Note required for all other exports and conversions**
* ExportKeybase.convert_json_to_sql(json_file, sql_connection_string)
* ExportKeybase.export_text_msgs_to_csv(sql_connection_string, output_file)
  * **Must has already exported from JSON to SQL**

## GeneratedAnalyitcs Class

### DATA

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
* GeneratedAnalytics.who_deletes_most_per_capita = {"users":{}, "ordered_users":[], "ordered_edit_per_capita" : []}
* GeneratedAnalytics.topic_edits_per_capita = {"topics":{}, "ordered_topics":[], "ordered_edit_per_capita" : []}
* GeneratedAnalytics.topic_deletes_per_capita = {"topics":{}, "ordered_topics":[], "ordered_edit_per_capita" : []}
* GeneratedAnalytics.top_domains = {"URLs":{}, "top_domains_sorted":[], "num_times_repeated":[]}

### Methods

* GeneratedAnalyitcs.get_message(MESSAGE_ID_NUM)
* GeneratedAnalyitcs.get_num_messages_from_user("USERS USERNAME") = {"edit": INT, "text": INT, "delete": INT}
* GeneratedAnalyitcs.get_num_messages_from_topic("TOPIC NAME") = {"edit": INT, "text": INT, "delete": INT}
* GeneratedAnalyitcs.get_reaction_poplarity_topic("TOPIC NAME") = {"reactions":{}, "list":[]}
* GeneratedAnalyitcs.get_all_user_message_id("USERS USERNAME") = {"users_reactions":{}, "users_ordered":[]}
* GeneratedAnalyitcs.get_reaction_type_popularity_per_user("USERS USERNAME") = {"users_reactions":{}, "reactions_ordered":[]}

## TODO

## Analitics

* Find the most URL's posted per user
* Finish the last couple methods in generate_analytics and then output their data in one or both of the jupyter notebooks
* Script to Export all attachments, must use keybase daemon
* Hook up the database to graphql
* Generate as many graphs as resonable using generate_graphs.ipynb

## Implimentaion Details

* Not importing Pin Message type because unable to find refence to message being pinned
* Not importing additional metadata such as device ID , device name, reactions within a message, and team_mentions though we may want to
* Wherever json.dumps is used in create_export it may not be desireable

## Problems moving forward

* How does this code scale to analyze multiple teams
* Real time export / Sync up without full export
* Coming up with Bot ideas for all this data
* Analysis functions to write
* reaction_poplarity_per_topic
  * user_recieved_most_reactions
  * reaction_type_popularity_per_user
  * Graph of activity over time
    * Total
    * Channel
    * User
    * User in Channel
    * Day of week
  * Average message length per
    * Channel
    * User
* Topic Modeling on channels and across channels
* Sentiment Analysis
* Machine Learning

## Tools moving forward

<https://www.nltk.org/>

## Library inspiration Stuff

* <https://github.com/keybase/pykeybasebot>
* <https://pypi.org/project/pykeybase/>
