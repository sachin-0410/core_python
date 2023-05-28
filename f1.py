import json

def print_all_keys(data, parent_key=''):
    if isinstance(data, dict):
        for key, value in data.items():
            if parent_key:
                nested_key = parent_key + '.' + key
            else:
                nested_key = key
            print_all_keys(value, nested_key)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            nested_key = parent_key + '[' + str(index) + ']'
            print_all_keys(item, nested_key)
    else:
        print(parent_key)

# Read the JSON file
with open('data.json') as file:
    json_data = json.load(file)

# Print all keys
print_all_keys(json_data)
