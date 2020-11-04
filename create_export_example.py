from create_export import ExportKeybase

print("Creating Keybase database export object...")
ex_key = ExportKeybase()
print("Exporting JSON file...")
ex_key.generate_json_export("complexweekend.oct2020", "complexityweekend.json")
print("Converting from JSON to SQLite...")
ex_key.convert_json_to_sql("./complexityweekend.json", "sqlite:///complexityweekend.sqlite")
print("All exports complete.")