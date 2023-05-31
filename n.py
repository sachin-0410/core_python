import requests
import time
import random
import json

def make_api_request(url, params=None):
    response = requests.get(url, params=params)
    response_data = response.json()
    return response_data

def process_api_response(response_data, file_path):
    # Process the response data here
    # ...

    # Write the response data to a local JSON file
    with open(file_path, 'w') as file:
        json.dump(response_data, file)

def get_data_with_pagination(url, params=None, file_path=None):
    max_retries = 5
    retry_count = 0
    backoff_time = 2  # Initial backoff time in seconds

    while url:
        try:
            response_data = make_api_request(url, params)
            process_api_response(response_data, file_path)

            # Check if there is a 'nextToken' in the response
            if 'nextToken' in response_data:
                next_token = response_data['nextToken']
                # Add 'nextToken' to the params for the next request
                params['nextToken'] = next_token
            else:
                # No more data available, exit the loop
                break

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 429:
                # Too Many Requests - Retry with exponential backoff
                if retry_count >= max_retries:
                    print("Max retries reached. Logging error and stopping.")
                    break

                wait_time = backoff_time + random.randint(1, 1000) / 1000.0
                print(f"Too Many Requests (HTTP 429) - Retry #{retry_count + 1}. Waiting for {wait_time:.2f} seconds.")
                time.sleep(wait_time)

                backoff_time *= 2
                retry_count += 1

            elif err.response.status_code == 403:
                # Limit Exceeded - Wait until after midnight to try again
                print("Limit Exceeded (HTTP 403). Waiting until after midnight to try again.")
                current_time = time.time()
                midnight_time = int(current_time) - (int(current_time) % 86400) + 86400  # Get the next midnight time
                wait_time = midnight_time - current_time
                time.sleep(wait_time)

            else:
                # Other HTTP errors
                print(f"HTTP Error: {err.response.status_code}")
                break

        except requests.exceptions.RequestException as err:
            # Other network or connection errors
            print(f"Request Exception: {err}")
            break

if __name__ == "__main__":
    api_url = "https://api.example.com/data"
    params = {
        # Set your desired parameters here
    }
    file_path = "/path/to/output.json"  # Replace with the desired output file path
    get_data_with_pagination(api_url, params, file_path)
