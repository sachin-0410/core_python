import requests
from datetime import datetime, timedelta

def get_monthly_data(start_date, end_date):
    url = "https://api.example.com/data"  # Replace with your API endpoint

    # Convert input date strings to datetime objects
    start_date = datetime.strptime(start_date, "%d%m%Y")
    end_date = datetime.strptime(end_date, "%d%m%Y")

    monthly_data = {}

    # Loop through monthly intervals and make API requests
    while start_date <= end_date:
        # Calculate the last day of the current month
        last_day_of_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

        # Format the date range for the API query
        query_start_date = start_date.strftime("%Y-%m-%d")
        query_end_date = last_day_of_month.strftime("%Y-%m-%d")

        # Set query parameters
        params = {
            "start_date": query_start_date,
            "end_date": query_end_date
        }

        # Make the API request
        response = requests.get(url, params=params)

        # Parse the response and extract the count
        data = response.json()
        count = data.get("count", 0)

        # Store the count for the current month
        month_name = start_date.strftime("%B %Y")
        monthly_data[month_name] = count

        # Move to the next month
        start_date = last_day_of_month + timedelta(days=1)

    return monthly_data

if __name__ == "__main__":
    # Example usage:
    start_date = "01-01-2021"
    end_date = "31-12-2021"

    monthly_data = get_monthly_data(start_date, end_date)

    # Print the monthly data
    for month, count in monthly_data.items():
        print(f"{month}: {count} entries")
