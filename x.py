import pandas as pd
import json

# Load the JSON data from the file
with open('test.json', 'r') as f:
    data = json.load(f)

# Create a DataFrame from the JSON data
df = pd.json_normalize(data)

# Display the DataFrame
print("DataFrame:")
print(df)

# Calculate the maximum length of data in each column
max_lengths = df.applymap(lambda x: len(str(x))).max()
print("\nMaximum length of data in each column:")
print(max_lengths)
