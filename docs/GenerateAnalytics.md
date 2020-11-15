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
