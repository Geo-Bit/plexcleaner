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
            "length": 100
        }
        
        try:
            print(f"Making API request to: {self.api_url}")
            print(f"With parameters: {params}")
            
            response = requests.get(self.api_url, params=params)
            
            print(f"Response status code: {response.status_code}")
            print(f"Response headers: {response.headers}")
            print("Response content:")
            print(response.text[:500])  # Print first 500 chars of response
            
            if response.status_code != 200:
                print(f"Error: API returned status code {response.status_code}")
                return []

            data = response.json()
            
            if "response" in data and "data" in data["response"]:
                return data["response"]["data"]
            else:
                print("Unexpected API response structure:")
                print(data)
                return []

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            print("Raw response:")
            print(response.text)
            return []
