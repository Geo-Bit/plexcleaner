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
        print(data)

        # Verify and return the 'data' field from the API response
        if "response" in data and "data" in data["response"]:
            return data["response"]["data"]
        else:
            print(f"Unexpected API response structure: {data}")
            return []
