import json
import openpyxl

# Function to extract all top-level and nested keys from a JSON object
def extract_json_keys(data, parent_key='', keys=[]):
    if isinstance(data, dict):
        for key, value in data.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, (dict, list)):
                extract_json_keys(value, new_key, keys)
            else:
                keys.append(new_key)
    elif isinstance(data, list):
        for item in data:
            extract_json_keys(item, parent_key, keys)
    return keys

# Function to extract columns from top-level and nested keys separately
def extract_columns(data):
    top_level_columns = []
    nested_columns = []

    for key in data:
        if '.' in key:
            nested_columns.append(key)
        else:
            top_level_columns.append(key)

    return top_level_columns, nested_columns

# Path to the JSON file
json_file_path = 'path/to/your/file.json'

# Load JSON data
with open(json_file_path) as json_file:
    json_data = json.load(json_file)

# Extract keys from JSON data
json_keys = extract_json_keys(json_data)

# Extract columns from top-level and nested keys separately
top_level_columns, nested_columns = extract_columns(json_keys)

# Print the top-level columns
print("Top-Level Columns:")
for column in top_level_columns:
    print(column)

# Print the nested columns
print("Nested Columns:")
for column in nested_columns:
    print(column)
