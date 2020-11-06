from create_export import ExportKeybase

print("Creating Keybase database export object...")
ex_key = ExportKeybase()
print("Exporting JSON file...")
ex_key.generate_json_export("dentropydaemon", "dentropydaemon.json")
print("Converting from JSON to SQLite...")
ex_key.convert_json_to_sql("./dentropydaemon.json", "sqlite:///dentropydaemon.sqlite")
print("All exports complete.")