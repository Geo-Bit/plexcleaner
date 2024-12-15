import requests

class TautulliAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get_watched_media(self):
        response = requests.get(f"{self.base_url}/api/v2", params={
            'apikey': self.api_key,
            'cmd': 'get_history',
            'length': 500
        })
        response.raise_for_status()
        return response.json().get('response', {}).get('data', [])
