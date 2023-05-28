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

# Function to extract all columns from an XLSX file
def extract_xlsx_columns(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    columns = []
    for column in sheet.iter_cols(min_row=1, max_row=1, values_only=True):
        columns.extend(column)
    return columns

# Path to the JSON file
json_file_path = 'path/to/your/file.json'
# Path to the XLSX file
xlsx_file_path = 'path/to/your/file.xlsx'

# Load JSON data
with open(json_file_path) as json_file:
    json_data = json.load(json_file)

# Extract keys from JSON data
json_keys = extract_json_keys(json_data)

# Extract columns from XLSX file
xlsx_columns = extract_xlsx_columns(xlsx_file_path)

# Compare the columns
common_columns = set(json_keys).intersection(set(xlsx_columns))
json_only_columns = set(json_keys).difference(set(xlsx_columns))
xlsx_only_columns = set(xlsx_columns).difference(set(json_keys))

# Print the results
print("Common Columns:")
print(common_columns)
print("JSON Only Columns:")
print(json_only_columns)
print("XLSX Only Columns:")
print(xlsx_only_columns)
