import requests
import json
import logging

# Set logging level to DEBUG to see more details
logging.basicConfig(level=logging.WARNING)

class TautulliAPI:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def get_watched_media(self):
        params = {
            "apikey": self.api_key,
            "cmd": "get_history",
            "length": 100,
            "include_media_info": 1  # Request additional media info
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
                
                # Get the media items
                media_items = data['response']['data']['data']
                
                # Get file paths for these items
                for item in media_items:
                    try:
                        file_params = {
                            "apikey": self.api_key,
                            "cmd": "get_metadata",
                            "rating_key": item['rating_key']
                        }
                        
                        file_response = requests.get(self.api_url, params=file_params)
                        if file_response.status_code == 200:
                            file_data = file_response.json()
                            logging.debug(f"Metadata response for {item['full_title']}: {json.dumps(file_data, indent=2)}")
                            
                            if ('response' in file_data and 
                                'data' in file_data['response'] and 
                                'media_info' in file_data['response']['data'] and
                                file_data['response']['data']['media_info']):  # Check if media_info is not empty
                                
                                media_info = file_data['response']['data']['media_info'][0]
                                if 'parts' in media_info and media_info['parts']:
                                    item['file'] = media_info['parts'][0]['file']
                                else:
                                    logging.warning(f"No parts found in media_info for: {item['full_title']}")
                                    item['file'] = None
                            else:
                                logging.warning(f"Incomplete metadata structure for: {item['full_title']}")
                                item['file'] = None
                        else:
                            logging.error(f"Failed to get metadata for {item['full_title']}: Status {file_response.status_code}")
                            item['file'] = None
                            
                    except Exception as e:
                        logging.error(f"Error getting file path for {item.get('full_title', 'unknown')}: {str(e)}")
                        item['file'] = None
                
                return media_items
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