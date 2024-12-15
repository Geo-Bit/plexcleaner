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

            data = response.json()
            
            # Log the structure of the response
            logging.debug(f"Response keys: {data.keys() if isinstance(data, dict) else 'not a dict'}")
            logging.debug(f"Response type: {type(data)}")
            
            if isinstance(data, dict) and "data" in data:
                return data["data"]
            else:
                logging.error("Unexpected API response structure")
                logging.error(f"Full response: {data}")
                return []

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return []
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing failed: {e}")
            return []
