import requests
import json
import logging

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
            response = requests.get(self.api_url, params=params)
            
            if response.status_code != 200:
                logging.error(f"Error: API returned status code {response.status_code}")
                return []

            # Check if we got HTML instead of JSON (indicates auth/login issue)
            if response.text.strip().startswith('<!doctype html>'):
                logging.error("Authentication error: Received login page instead of API data")
                logging.error("Please check your Tautulli API URL and API key")
                return []

            try:
                data = response.json()
                if isinstance(data, dict) and "data" in data:
                    return data["data"]
                else:
                    logging.error("Unexpected API response structure")
                    logging.debug(f"Response: {data}")
                    return []

            except json.JSONDecodeError:
                logging.error("Failed to parse JSON response")
                logging.debug(f"Raw response: {response.text[:1000]}")  # Log first 1000 chars
                return []

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return []
