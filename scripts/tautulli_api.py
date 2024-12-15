import requests
import json

class TautulliAPI:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_watched_media(self):
        params = {
            "apikey": self.api_key,
            "cmd": "get_history",
            "length": 100  # Adjust length as needed
        }
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Log the raw response text
            print("Raw API Response:")
            print(response.text)

            # Attempt to parse JSON response
            data = response.json()
            print("Parsed JSON Response:")
            print(data)

            # Extract the data if the structure matches
            if "response" in data and "data" in data["response"]:
                return data["response"]["data"]  # Return the media list
            else:
                print("Unexpected API response structure")
                return []

        except json.JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
            print("Non-JSON response:")
            print(response.text)
            return []

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []
