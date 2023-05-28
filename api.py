import requests
import json
import time

def retrieve_access_token():
    # Implement your logic to retrieve the access token here
    # This can involve authentication, such as OAuth or API key

    # Example code using OAuth2 and requests library
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    auth_url = 'https://example.com/oauth/token'
    data = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}

    response = requests.post(auth_url, data=data)
    response_json = response.json()
    access_token = response_json['access_token']
    
    return access_token

def call_api_with_pagination(access_token):
    api_url = 'https://example.com/api/endpoint'
    local_path = 'response.json'
    limit = 10  # Maximum number of API calls
    wait_time = 1  # Wait time in seconds between API calls
    next_token = None
    total_calls = 0

    try:
        while True:
            headers = {'Authorization': f'Bearer {access_token}'}
            params = {'next_token': next_token} if next_token else {}

            response = requests.get(api_url, headers=headers, params=params)
            response_json = response.json()

            # Write response to local file
            with open(local_path, 'a') as file:
                json.dump(response_json, file)
                file.write('\n')

            total_calls += 1

            if 'next_token' in response_json and total_calls < limit:
                next_token = response_json['next_token']
                time.sleep(wait_time)  # Wait before making the next API call
            else:
                break

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print(f"API calls completed. Total calls made: {total_calls}")

# Usage
access_token = retrieve_access_token()
call_api_with_pagination(access_token)
