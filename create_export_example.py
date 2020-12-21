from database import Messages, Users
from create_export import ExportKeybase

keybase_team = "dentropydaemon" # Change this to export a different team
print("Creating Keybase database export object...")
ex_key = ExportKeybase()
print("Exporting JSON file...")
ex_key.generate_json_export(keybase_team, "./exports/%s-messages.json" % keybase_team)
print("Getting user metadata and dumping to SQLite...")
ex_key.export_team_user_metadata_sql(keybase_team, "sqlite:///exports/%s.sqlite" % keybase_team)
print("Getting user metadata and dumping to SQLite...")
ex_key.generate_sql_export(keybase_team, "sqlite:///exports/%s.sqlite" % keybase_team)
print("Finished getting the messages and putting them in the databse.")
ex_key.message_table_to_csv(Messages, "sqlite:///exports/%s.sqlite" % keybase_team, "./exports/%s-messages.csv" % keybase_team)
print("Exporting Users table to CSV")
ex_key.message_table_to_csv(Users, "sqlite:///exports/%s.sqlite" % keybase_team, "./exports/%s-users.csv" % keybase_team)
print("Exporting Messages table to CSV")
print("All exports complete.")
