import requests

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
        response = requests.get(self.api_url, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()  # Parse JSON response

        # Log the full response for debugging
        print("Full API Response:")
        print(data)

        if "response" in data and "data" in data["response"]:
            return data["response"]["data"]  # This should return the media list
        else:
            print("Unexpected API response structure")
            return []
