import os

class Config:
    def __init__(self):
        self.tautulli_url = os.getenv('TAUTULLI_URL')
        self.api_key = os.getenv('TAUTULLI_API_KEY')
        self.days_since_watched = int(os.getenv('DAYS_SINCE_WATCHED', 30))
        self.unwatched_cutoff = int(os.getenv('UNWATCHED_CUTOFF', 180))
        self.tv_directory = os.getenv('TV_DIRECTORY', '/media/TV')
