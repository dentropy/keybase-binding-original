### `ExportKeybase` Class

> _Python3 class to generate lists of information via direct interface to `Keybase`._
> *Lives in [`create_export.py`](create_export.py).*

#### `ExportKeybase` Methods ####

This class contains a list of tools for exporting and transforming various types of information from keybase. So far we can export team chat logs with attachments, and user metadata such as what teams they are on, users they follow, users that follow them and where they have verified their identity such as twitter and facebook.

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