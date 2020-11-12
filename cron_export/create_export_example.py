import sys
sys.path.append("..")
from database import Messages
from create_export import ExportKeybase


print("Creating Keybase database export object...")
ex_key = ExportKeybase()
print("Exporting JSON file...")
ex_key.generate_json_export("dentropydaemon", "./" + sys.argv[1] + "/dentropydaemon.json")
print("Converting from JSON to SQLite...")
ex_key.convert_json_to_sql("./" + sys.argv[1] + "/dentropydaemon.json",  "sqlite:///"+sys.argv[1]+"/dentropydaemon.sqlite")
print("Exporting Messages table to CSV")
ex_key.message_table_to_csv(Messages, "sqlite:///"+sys.argv[1]+"/dentropydaemon.sqlite",  "./" +  sys.argv[1] + "/dentropydaemon.csv")
print("All exports complete.")