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

            data = response.json()
            
            # Navigate through the nested structure
            if (isinstance(data, dict) and 
                'response' in data and 
                'data' in data['response'] and 
                'data' in data['response']['data']):
                
                return data['response']['data']['data']
            else:
                logging.error("Unexpected API response structure")
                logging.debug(f"Response structure: {data.keys() if isinstance(data, dict) else type(data)}")
                return []

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            return []
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing failed: {e}")
            return []