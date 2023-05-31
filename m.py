def get_access_token():
    config = read_config()
    auth_url = config['authentication_url']
    client_id = config['client_id']
    client_secret = config['client_secret']

    response = requests.post(auth_url, data={'client_id': client_id, 'client_secret': client_secret})

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    elif response.status_code == 429:
        print("Too Many Requests. Retrying with exponential backoff...")
        wait_time = 2  # initial wait time in seconds
        attempt = 1
        while attempt <= 5:
            print(f"Attempt #{attempt}")
            time.sleep(wait_time + random.randint(1, 1000) / 1000)  # add random milliseconds to wait time
            response = requests.post(auth_url, data={'client_id': client_id, 'client_secret': client_secret})
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                return access_token
            elif response.status_code == 429:
                wait_time *= 2  # double the wait time on each subsequent attempt
                attempt += 1
            else:
                break
        print("Exceeded maximum retry attempts. Please try again later.")
        raise Exception("Too Many Requests")
    elif response.status_code == 503:
        print("API service unavailable. Please try again later.")
        raise Exception("Service Unavailable")
    else:
        print(f"Authentication failed. Status code: {response.status_code}")
        raise Exception("Authentication failed.")
