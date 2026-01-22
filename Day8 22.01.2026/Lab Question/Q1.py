# Write a Python program that:
# 1. Uses the requests library to send a GET request to a public REST API (e.g., users or posts API)
# 2. Sends custom headers with the request
# 3. Parses the JSON response and extracts specific fields
# 4. Serializes the extracted data and saves it into a JSON file
# 5. Handles HTTP errors using proper exception handling

import requests
import json


def fetch_and_save_users():
    # 1. Define the API endpoint
    url = "https://jsonplaceholder.typicode.com/users"

    # 2. Define custom headers
    # Many APIs require an Authorization header or specific User-Agent
    headers = {
        "User-Agent": "PythonRequestScript/1.0",
        "Accept": "application/json",
        "Authorization": "Bearer sample_token_123",
    }

    try:
        # 3. Send GET request
        print(f"Sending request to {url}...")
        response = requests.get(url, headers=headers, timeout=10)

        # 4. Handle HTTP errors
        response.raise_for_status()

        # 5. Parse JSON response
        users_data = response.json()
        print(f"Successfully retrieved {len(users_data)} records.")

        # 6. Extract specific fields
        extracted_data = []
        for user in users_data:
            user_info = {
                "user_id": user.get("id"),
                "full_name": user.get("name"),
                "email_address": user.get("email"),
            }
            extracted_data.append(user_info)

        # 7. Serialize and save to a JSON file
        output_filename = "filtered_users.json"
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, indent=4)

        print(f"Data successfully saved to '{output_filename}'.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")
    except IOError as io_err:
        print(f"File handling error: {io_err}")


if __name__ == "__main__":
    fetch_and_save_users()
