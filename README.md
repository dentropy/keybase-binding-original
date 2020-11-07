# `Keybase` Text Chat Data

This repository contains code for Python3, Matlab, and Obsidian, which can be used to access the `Keybase` text chat API, scrape user metadata and text message information, perform analyses on that data, and visualize the resulting social network graph.

## Installation

> *What do I need to install to make use of the code contained in this repository?* 
> *How do I go about doing that?*

### Requirements

#### Python 3 ####

* [`Anaconda` data science tool box](https://www.anaconda.com/products/individual), with the following packages installed:
  * [`sqlalchemy`](https://www.sqlalchemy.org/download.html): A Python SQL interface for database creation, access, and management.
  * [`matplotlib`](https://matplotlib.org/3.3.2/users/installing.html):  A Python library for creating visualizations of data.
  * [`jupyter notebook`](https://jupyter.org/install): A Python notebook for inline markdown annotation of analyses.
* Additional [`pip`](https://docs.python.org/3/installing/index.html) packages
  * [`tld`](https://pypi.org/project/tld/): Python package for extracting top-level domain (TLD) from text.
  * [`URLExtract`](https://pypi.org/project/urlextract/): Python package for extracting URLs based on TLD.

#### MATLAB ####

* All **[`MATLAB`](https://www.mathworks.com/)** analyses were conducted in version *R2020b*, with the full suite of toolboxes installed. None of it is core or essential to looking at these data, but it's an option if you have access to the toolboxes. 

#### Applications ####

* **[`Keybase`](https://keybase.io/download)** (encrypted, open-source text chat platform)
  * To extract text data, the user must be logged into `Keybase` (and can only extract data from text "visible" to that user specifically).
  * *Note: because `Keybase` was recently acquired by `Zoom`, this may only be a temporary solution.*
* **[`Obsidian`](https://obsidian.md/)** (markdown editor)

---

## Use ##

> *How do I make use of the code in this repository?*

Getting started is a two-step process. First, you need to get access to the data (whether in `.json`, `.sqlite`, or `.csv`). This can be done by either copying an exported version of one of the data files from the shared `Keybase` team `Files` storage, or by [exporting](#exporting-data) your own copy as described below. Once the data has been exported, analyses are conducted via an object-oriented workflow, preferably in a `Jupyter` notebook (`.ipynb` files, as described [below](#open-the-jupyter-notebook)). See class [documentation](#analysis-class-documentation) for object property and method details.

#### TODO ####

- [ ] *Fix public/private scoping on class properties and methods.*

### Exporting Data

In the terminal, navigate to the folder containing [`create_export_example.py`](create_export_example.py), and execute the following commands:

``` bash
pip3 install URLExtract
python3 create_export_example.py
```
If you want to change the `Keybase` team, export `json` file, or `sqlite json` file you can do so in the last two lines of the [`create_export.py`](create_export.py) file.

#### TODO ####

- [ ] *Create a bot that automatically appends data to the `.sqlite` database with each new message on text channels it "lives" in.*

## Open the Jupyter Notebook

Navigate to this directory using the command line and run the following command,

``` bash
jupyter notebook
```

Your browser should open with a listing of the files associated with this project. Open [`generate_analytics.py`](generate_analytics.py) and have fun.

#### TODO ####

- [ ] *Use something like the `plotly` package to turn existing `Jupyter` notebooks into embeddable (or linkable) dashboards, which can then be accessed from the **[wiki](https://wiki.dentropydaemon.io/Dashboards)**, embedded in a local application, or hosted elsewhere?*

## Analysis Class Documentation ##

The Python analysis pipeline is object-oriented. Three `Python` classes run most of the methods:

* **[`ExportKeybase`](#exportkeybase-class)**: Python3 class to generate lists of information via direct interface to `Keybase`.

  * Lives in [`create_export.py`](create_export.py)

  * Import using:

    ```python
    from create_export import ExportKeybase
    ```

* **[`GenerateAnalytics`](#generateanalytics-class)**: Python3 class to organize different kinds of data from `Keybase` export.

  * Lives in [`generate_analytics.py`](generate_analytics.py)

  * Import using:

    ```python
    from generate_analytics import GeneratedAnalytics
    ```

* **[`Messages`](#messages-class)**: Python3 class that uses `sqlalchemy` to interface with `SQL` database.

  * Lives in [`database.py`](database.py)

  * Import using:

    ```python
    from database import Messages
    ```

    * *Note: this is a simpler class that really only has a constructor and properties related to the variables of interest that are extracted from the `Keybase` data.*

---

### `ExportKeybase` Class

> _Python3 class to generate lists of information via direct interface to `Keybase`._
> *Lives in [`create_export.py`](create_export.py).*

#### `ExportKeybase` Methods ####

Prior to running any other method, you must first **[export](#generate_json_export)** a `.json` file containing the text chat data (provided that no `.json` file has been exported previously or that you did not copy a `.json` file from elsewhere). Similarly, any method that interfaces to an `SQL` database requires **[conversion](#convert_json_to_sql)** from `.json` to `.sqlite` prior to running.

##### `generate_json_export` #####

```python
ExportKeybase.generate_json_export(keybase_team, output_file)
```

Creates a `.json` file named `output_file` containing all chat messages from an entire team.

* **Output `.json` file is required for all other methods in this class!**

##### `convert_json_to_sql` #####

```python
ExportKeybase.convert_json_to_sql(json_file, sql_connection_string)
```

Convert `.json` file data to SQL database structure.

* **Output `.sqlite` file is required for any method involving `SQL` database ([`Messages`](#messages-class) class object imported from [`database.py`](database.py)).**

##### `get_teams` #####

```python
 `teams = ExportKeybase.get_teams()`
```

Returns string list `teams` corresponding to each unique team for which the current `Keybase` user is a member. Must be logged into `Keybase`.

##### `get_team_memberships`

```python
usernames = ExportKeybase.get_team_memberships(team_name)
```

Returns string list `usernames` of usernames on that team

##### `get_user_metadata` #####

```python
user_metadata = ExportKeybase.get_user_metadata(username)
```

Returns string list `user_metadata` of URLs where user has verified their `Keybase` identity plus all teams they are on.

##### `export_team_user_metadata` #####

````python
members = ExportKeybase.export_team_user_metadata()
````

Write a `.json` file of all users, where they are verified, and what teams they belong to.

###### TODO ######

- [ ] **Change so it returns an object instead of writing to disk.**

##### `get_team_channels` #####

````python
mah_channels = ExportKeybase.get_team_channels(keybase_team_name)
````

Returns list of strings `mah_channels` for each text channel on a team

##### `get_team_chat_channel` #####

```python
obj = ExportKeybase.get_team_chat_channel(keybase_team_name, keybase_topic_name)
```

Returns [`obj`](https://docs.python.org/3/library/json.html), a `json` [object](https://docs.python.org/3/library/json.html) of all messages within a `Keybase` team topic.

##### `get_root_messages` #####

```python
ExportKeybase.get_root_messages(mah_messages, db)
```

Finds text messages from input message list `mah_messages`, adds them to the SQL database session `db`, then commits the session.

###### TODO ######

- [ ] **Interface this function to custom `pykeybasebot` to implement database update.**

##### `get_reaction_messages` #####

```python
ExportKeybase.get_reaction_messages(mah_messages, db)
```

Finds reactions from input message list `mah_messages`, adds them to the SQL database session `db`, then commits the session.

###### TODO ######

- [ ] **Interface this function to custom `pykeybasebot` to implement database update.**

##### `export_text_msgs_to_csv` #####

```python
ExportKeybase.export_text_msgs_to_csv(sql_connection_string, output_file)
```

Export text messages from `.sqlite` database to `.csv` spreadsheet specified by `output_file`.

* ***Note:*** *requires previous [export](#convert_json_to_sql) from `.json` to `.sql`.*

##### `message_table_to_csv` #####

```python
ExportKeybase.message_table_to_csv(table_object, sql_connection_string, csv_file_name)
```

Export [table](https://python-docx.readthedocs.io/en/latest/api/table.html) object `table_object` with text message data to `.csv` spreadsheet.

---

### `GeneratedAnalytics` Class

> _Python3 class to organize different kinds of data from `Keybase` export._
> *Lives in [`generate_analytics.py`](generate_analytics.py).*

#### `GeneratedAnalytics` Properties

The properties of the `GeneratedAnalytics` class are maybe best to think of as "data reports." `GeneratedAnalytics` "reports" are refreshed by corresponding **[Methods](#generatedanalytics-methods)**.

##### `user_list` #####

```python
GeneratedAnalytics.user_list = []
```

A `list` containing `string` elements that are the unique users in the database.

##### `topic_list` #####

```
GeneratedAnalytics.topic_list = []
```

A `list` containing `string` elements that are the unique topics in the database.

##### `topic_list` #####

```python
GeneratedAnalytics.characters_per_user = {"user": [], "characters_per_user": []}
```

A `dict` array with the total number of characters entered via messages to chat by element in [`user_list`](#user_list).

##### `characters_per_topic` #####

```
GeneratedAnalytics.characters_per_user = {"user": [], "characters_per_topic": []}
```

A `dict` array with the total number of characters per element in [`topic_list`](#topic_list).

##### `messages_per_user` #####

```python
GeneratedAnalytics.messages_per_user = {"user": [], "messages_per_user": []}
```

A `dict` array with the total number of messages to chat by element in [`user_list`](#user_list).

##### `messages_per_topic` #####

```python
GeneratedAnalytics.messages_per_topic = {"topic": [], "messages_per_topic": []}
```

A `dict` array with the total number of messages per element in [`topic_list`](#topic_list).

##### `number_users_per_topic` #####

```python
GeneratedAnalytics.number_users_per_topic = {"users_list": [], "topics_list": []}
```

A `dict` array with the number of users per element  in [`topic_list`](#topic_list).

##### `reaction_per_message` #####

```python
GeneratedAnalytics.reaction_per_message = {"ordered_message_id":[], "num_reaction":[]}
```

A `dict` array with the message ID and corresponding number of reactions to that message.

##### `reaction_sent_per_user` #####

```python
GeneratedAnalytics.reaction_sent_per_user = {"ordered_user":[], "user_to_reaction":[]}
```

###### TODO ######

- [ ] *Check that this is actually what we think it is. Looks like User gets sorted, but `user_to_reaction` is not?*

##### `reaction_popularity_map` #####

```python
GeneratedAnalytics.reaction_popularity_map = {"reactions":{}}
```

###### TODO ######

- [ ] *Clarify what this is (or remove)?*

##### `reactions_per_user` #####

```python
GeneratedAnalytics.reactions_per_user = {"users_reactions":{}, "users_ordered":[]}
```

###### TODO ######

- [ ] *Clarify what this is: lists of unique reactions per user?*

##### `received_most_reactions` #####

```python
GeneratedAnalytics.recieved_most_reactions = {"users_reactions":{}, "users_ordered":[]}
```

###### TODO ######

- [ ] *Clarify what this is: list of messages with most reactions by user and what the reactions were?*

##### `edits_per_user` #####

```python
GeneratedAnalytics.edits_per_user = {
    "users":{}, 
    "ordered_users":[], 
    "ordered_num_edits":[]}
```

Which user had the most (raw) number of edits?

##### `edits_per_topic` #####

```
GeneratedAnalytics.edits_per_topic = {
"topics":{}, 
"ordered_topics":[], 
"ordered_num_edits":[]}
```

Which topic had the most (raw) number of edits?

##### `deletes_per_user` #####

```python
GeneratedAnalytics.deletes_per_user = {
"users":{}, 
"ordered_users":[], 
"ordered_num_deletes":[]}
```

Which users had the most (raw) number of deletes?

##### `deletes_per_topic` #####

```python
GeneratedAnalytics.deletes_per_topic = {
"topics":{}, 
"ordered_topics":[], 
"ordered_num_deletes":[]}
```

Which topics had the most (raw) number of deletes?

##### `who_edits_most_per_capita` #####

```python
GeneratedAnalytics.who_edits_most_per_capita = {
    "users":{}, 
    "ordered_users":[], 
    "ordered_edit_per_capita" : []}
```

Who edits most per message?

##### `who_deletes_most_per_capita` #####

```python
GeneratedAnalytics.who_deletes_most_per_capita = {
    "users":{}, 
    "ordered_users":[], 
    "ordered_edit_per_capita" : []}
```

Who deletes the most per message?

##### `topic_edits_per_capita` #####

```python
GeneratedAnalytics.topic_edits_per_capita = {
    "topics":{}, 
    "ordered_topics":[], 
    "ordered_edit_per_capita" : []}
```

Which topic channels had the most edits per message?

##### `topic_deletes_per_capita` #####

```python
GeneratedAnalytics.topic_deletes_per_capita = {
    "topics":{}, 
    "ordered_topics":[], 
    "ordered_edit_per_capita" : []}
```

Which topic channels had the most deletes per message?

##### `top_domains` #####

```python
GeneratedAnalytics.top_domains = {
    "URLs":{}, 
    "top_domains_sorted":[], 
    "num_times_repeated":[]}
```

What were the most-used top-level domains, what were the specific links, and how many times did they appear?

---

##### `GeneratedAnalytics` Methods

Methods are mainly there to return "refreshed" versions of the data with respect to the database.

##### `get_message` #####

```python
message = GeneratedAnalytics.get_message(MESSAGE_ID_NUM)
```

Returns a single row from Message object (SQL table) by ID.

##### `get_reaction_per_message` #####

```python
GeneratedAnalytics.get_reaction_per_message()
```

Update the reactions to each message.

##### `get_reaction_sent_per_user` #####

```python
GeneratedAnalytics.get_reaction_sent_per_user()
```

Update the reactions sent by each user.

##### `get_num_messages_from_user` #####

```python
msg_changes = {"edit": INT, "text": INT, "delete": INT}
msg_changes.append(GeneratedAnalytics.get_num_messages_from_user("USER"))
```

Return object with number of times a text was edited or deleted for a given user.

##### `get_num_messages_from_topic` #####

```python
messages = {"edit": INT, "text": INT, "delete": INT}
messages.append(GeneratedAnalytics.get_num_messages_from_topic("TOPIC"))
```

Return object with number of times a text was edited or deleted for a given topic.

##### get_list_all_users #####

```python
GeneratedAnalytics.get_list_all_users()
```

Should be called from the object constructor; updates and returns list of all users in database.

###### TODO ######

- [ ] *Set scoping for private/public methods?*

##### get_list_all_topics #####

```python
GeneratedAnalytics.get_list_all_topics()
```

Should be called from the object constructor; updates and returns list of all topics in database.

###### TODO ######

- [ ] *Set scoping for private/public methods?*

##### `get_characters_per_user` #####

```python
characters_per_user = {"user": [], "characters_per_user": []}
characters_per_user.append(GeneratedAnalytics.get_characters_per_user())
```

Update and return total number of characters from messages for each user.

###### TODO ######

- [ ] *Set scoping for private/public methods?*

##### `get_characters_per_topic` #####

```python
characters_per_topic = {"user": [], "characters_per_topic": []}
characters_per_topic.append(GeneratedAnalytics.get_characters_per_topic())
```

Update and return total number of characters from messages posted in each topic.

###### TODO ######

- [ ] *Set scoping for private/public methods?*

##### `get_messages_per_user` #####

```python
messages_per_user = {"user": [], "messages_per_user": []}
messages_per_user.append(GeneratedAnalytics.get_messages_per_user())
```

Update and return total number of messages for each user.

###### TODO ######

- [ ] *Set scoping for private/public methods?*

##### `get_messages_per_topic` #####

```python
messages_per_topic = {"user": [], "messages_per_topic": []}
messages_per_topic.append(GeneratedAnalytics.get_messages_per_topic())
```

Update and return total number of messages posted in each topic.

###### TODO ######

- [ ] *Set scoping for private/public methods?*

##### get_number_users_per_topic #####

```python
number_users_per_topic = {"users_list": [], "topics_list": []}
number_users_per_topic.append(
    GeneratedAnalytics.get_number_users_per_topic)
```

Update and return the number of users for each topic.

###### TODO ######

- [ ] *Set scoping for private/public methods?*

##### `get_reaction_popularity_topic` #####

```python
reactions = {"reactions":{}, "list":[]}
reactions.append(GeneratedAnalytics.get_reaction_popularity_topic("TOPIC"))
```

Get popularity of all reactions in a topic corresponding to a specific topic (`string`).

##### `get_all_user_message_id` #####

```python
msgID = {"users_reactions":{}, "users_ordered":[]}
msgID.append(GeneratedAnalytics.get_all_user_message_id(user))
```

For a specific user (`user`, `string`), return all message IDs involving that user.

##### `get_user_sent_most_reactions` #####

```python
GeneratedAnalytics.get_user_sent_most_reactions()
```

Return the sorted user by most number of reactions issued.

##### `get_user_received_most_reactions` #####

```python
GeneratedAnalytics.get_user_received_most_reactions()
```

Update and return the sorted listing of users by number of reactions received.

##### `get_edits_per_user` #####

```python
GeneratedAnalytics.get_edits_per_user()
```

Update and return the raw number of edited messages by user.

##### `get_deletes_per_user` #####

```python
GeneratedAnalytics.get_deletes_per_user()
```

Update and return the raw number of deleted messages by user.

##### `get_edits_per_topic` #####

```python
GeneratedAnalytics.get_edits_per_topic()
```

Update and return the raw number of edited messages by topic.

##### `get_deletes_per_topic` #####

```python
GeneratedAnalytics.get_deletes_per_topic()
```

Update and return the raw number of deleted messages by topic.

##### `get_who_edits_most_per_capita` #####

```python
GeneratedAnalytics.get_who_edits_most_per_capita()
```

Update and return the sorted per-capita message edits by user.

##### `get_who_deletes_most_per_capita` #####

```python
GeneratedAnalytics.get_who_deletes_most_per_capita()
```

Update and return the sorted per-capita message deletions by user.

##### `get_topic_edits_per_capita` #####

```python
GeneratedAnalytics.get_topic_edits_per_capita()
```

Update and return the per-capita edits by topic.

##### `get_topic_deletes_per_capita` #####

```python
GeneratedAnalytics.get_topic_deletes_per_capita()
```

Update and return the per-capita deletes by topic.

##### `get_top_domains` #####

```python
GeneratedAnalytics.get_top_domains()
```

Update list of most-popular top-level domains linked in text chat.

##### `get_reaction_type_popularity_per_user` #####

```python
reaction_type_popularity_per_user = {
    "users_reactions":{},
    "reactions_ordered":[]
}
reaction_type_popularity_per_user.append(
    GeneratedAnalytics.get_reaction_type_popularity_per_user(
        "USERS USERNAME"))
```

Returns/updates the popularity of a given reaction type by their username.

##### `get_message_data_frames` #####

```python
df = get_message_data_frames(self, offset_time=0)
```

Returns `df`, a [`Pandas`](https://pandas.pydata.org/getting_started.html) data frame with user, message ID, time, team name, topic, body text, and word count data for `"text"` type messages only.

---

### `Messages` Class ###

> _Python3 class that uses `sqlalchemy` to interface with `SQL` database._
> *Lives in [`database.py`](database.py).*

#### `Messages` Properties ####

Each `Messages` property can be thought of like a table column. They correspond to parts of the `.json` object returned by querying `Keybase` that we want to retain about each message, which includes transactions like "reactions" to other text chat messages, or users entering and leaving a channel.

##### `id` #####

```python
id = Column(Integer, primary_key=True)
```

Primary key identifier for each unique Message.

##### `team` #####

```python
team = Column(String(1024))
```

Which `Keybase` team was this message sent in?

##### `topic` #####

```python
topic = Column(String(128))
```

What Topic channel was this  message sent in?

##### `msg_id`

```python
msg_id = Column(Integer)
```

What message does this instance reference?

##### `msg_type`

```python
msg_type = Column(String(32))
```

What type of message (i.e. "text", "reaction", etc.) was this interaction?

##### `from_user`    

```python
from_user = Column(String(128))
```

From which user did this message originate?

##### `sent_time`    

```python
sent_time = Column(Integer)
```

What time was this message sent?

* *Note: this is the number of seconds, in posixtime convention (UTC). That is, the number of seconds elapsed since 1970.*

##### `txt_body`

```python
txt_body = Column(String(4096))
```

What text content was in the body of the message?

##### `word_count` #####

```python
word_count = Column(Integer)
```

How many words are in the body of the message?

###### TODO ######

- [ ] *Indicate how this was computed; are stop words included? etc.*

##### `num_urls`

```python
num_urls = Column(Integer)
```

How many URLs are referenced in this message?

##### `urls`

```python
urls = Column(String(4096))
```

What URLs were identified in this message?

###### TODO ######

- [ ] *Indicate how this was computed: are the URLs recognized on the Keybase end or on our side? From the code it looks like it is done on their end.*

##### `reaction_body`

```python
reaction_body = Column(String(1024))
```

If this is a reaction message, what emoji reaction was used in response to the message?

##### `msg_reference`

```python
msg_reference = Column(Integer)
```

If this message replies to (for `"text"`) or reacts to (for `"reaction"`), which message identifier does it reference?

##### `userMentions`

```python
userMentions = Column(String(1024))
```

What users were `@<user>` tagged in this message?

---

## TODO

> *What remains to be done on this project?*

### Analytics

*Open problems remaining for analyzing existing data.*

#### Questions ####

*Questions or tasks requiring interaction with the data to generate actionable insight.*

- [ ] Describe the distribution of number of URLs posted by user. 
- [x] Finish the last couple methods in `generate_analytics.py` and then output their data in one or both of the `jupyter` notebooks
- [ ] Script to Export all attachments, must use `Keybase` daemon
- [ ] Hook up the database to `graphql`
- [ ] Generate as many graphs as reasonable using **[`generate_graphs.ipynb`](generate_graphs.ipynb)**

#### Graphics ####

_List of graphics/kinds of data we still need to visualize._

Graph of [*data*] [*type*] broken down by [*view*], where [*type*] is:

- [ ] Total
- [ ] Channel
- [ ] User
- [ ] User in Channel
- [ ] Day of week

##### Example of "Activity" proxy #####

Average message length per

- [ ] Channel
- [ ] User

---

### Development

*What remains to be done with respect to writing more code and other dev-ops tasks?*

* How does this code scale to analyze multiple teams

* **Real time export / Sync up without full export**

* Coming up with Bot ideas for all this data

* Analysis functions to write

  - [ ] `reaction_popularity_per_topic` 

  * [ ] `user_recieved_most_reactions` 
  * [ ] `reaction_type_popularity_per_user` 

---

## Notes ##

*Miscellaneous observations during development.*

### Regarding Implementation

- **We currently do not (but could):**
  - Import Pin Message type because unable to find refence to message being pinned.
  - Import additional metadata such as: 
    - `device ID` 
    - `device name` 
    - `reactions within a message` 
    - `team_mentions` 
- **We could improve:**
  - Wherever `json.dumps` is used in [`create_export.py`](create_export.py), it may not be desirable.

### Regarding Data-Driven Models ###

* **Topic Modeling on channels and across channels**
  * *Can we train a simple Linear Discriminant Analysis (LDA) model on channel-based text messages in order to get "good" separation of channels that do not have much overlap based on what we know and understand about language already?*
    * *Based on the training data that we have available to perform such a task, do we expect there to be "good" separation of topics by channel from the Complexity Weekend Keybase text database?*
    * *Do we need a different dataset for **Topic Modeling** altogether?*
* **Sentiment Analysis**
  * *Why does the **VADER** algorithm think that **Jason's** `Keybase` profile has such a negative sentiment score? Are there other better algorithms? Is there a list of other algorithms and links to source documentation or (even better) related literature to cite?*
* ~~Machine Learning~~

---

## Links

*Assorted links to tools and readings.*

### Tools moving forward

* **[`NLTK`](https://www.nltk.org/)**: Open-source natural language toolkit.
* **[`spaCy`](https://spacy.io/)**: Natural language processing (NLP) API that still provides many useful free tools.
* **[`kumo.io`](https://kumo.io/)**: Interactive network graph visualization tool with easy Import/Export format (and supports export of embedded views).

### Relevant External Libraries

* [PyKeybase Library](https://pypi.org/project/pykeybase/)
* [PyKeybaseBot GitHub Repository](https://github.com/keybase/pykeybasebot)

### Other ###

* **[Dentropy Daemon Wiki](https://wiki.dentropydaemon.io/)**
  * [Dashboards](https://wiki.dentropydaemon.io/en/Dashboards)

