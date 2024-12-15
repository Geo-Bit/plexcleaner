import requests
import json
import logging

# Set logging level to DEBUG to see more details
logging.basicConfig(level=logging.DEBUG)

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
            logging.debug(f"Making request to: {self.api_url}")
            response = requests.get(self.api_url, params=params)
            
            if response.status_code != 200:
                logging.error(f"Error: API returned status code {response.status_code}")
                return []

            # Check if we got HTML instead of JSON
            if response.text.strip().startswith('<!doctype html>'):
                logging.error("Authentication error: Received login page instead of API data")
                logging.error("Please check your Tautulli API URL and API key")
                return []

            try:
                data = response.json()
                logging.debug(f"Response data structure: {data.keys() if isinstance(data, dict) else type(data)}")
                
                if isinstance(data, dict) and "data" in data:
                    logging.debug(f"Found data array with {len(data['data'])} items")
                    return data["data"]
                else:
                    logging.error("Unexpected API response structure")
                    logging.error(f"Full response: {data}")
                    return []

            except json.JSONDecodeError:
                logging.error("Failed to parse JSON response")
                logging.error(f"Raw response text: {response.text[:500]}...")
                return []

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return []