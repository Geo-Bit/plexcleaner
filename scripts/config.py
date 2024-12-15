import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    TAUTULLI_URL = os.getenv('TAUTULLI_URL')
    TAUTULLI_API_KEY = os.getenv('TAUTULLI_API_KEY')
    DAYS_SINCE_WATCHED = int(os.getenv('DAYS_SINCE_WATCHED', 30))
    UNWATCHED_CUTOFF = int(os.getenv('UNWATCHED_CUTOFF', 180))
    MOVIES_DIR = os.getenv('MOVIES_DIRECTORY', '/media/Movies')
