from database import Messages, Users
from create_export import ExportKeybase

print("Creating Keybase database export object...")
ex_key = ExportKeybase()
print("Exporting JSON file...")
ex_key.generate_json_export("dentropydaemon", "dentropydaemon.json")
print("Converting from JSON to SQLite...")
ex_key.convert_json_to_sql("./dentropydaemon.json", "sqlite:///dentropydaemon.sqlite")
print("Getting user metadata and dumping to SQLite...")
ex_key.export_team_user_metadata_sql("dentropydaemon", "sqlite:///dentropydaemon.sqlite")
print("Exporting Messages table to CSV")
ex_key.message_table_to_csv(Messages, "sqlite:///dentropydaemon.sqlite", "dentropydaemon.csv")
print("All exports complete.")
ex_key.message_table_to_csv(Users, "sqlite:///dentropydaemon.sqlite", "keybase-users.csv")
print("All exports complete.")
