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