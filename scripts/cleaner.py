import os
import logging
from datetime import datetime, timedelta
from tautulli_api import TautulliAPI
from config import Config
from logger import setup_logger

logger = setup_logger()

def main():
    # Instantiate the TautulliAPI class
    api = TautulliAPI(api_url=Config.TAUTULLI_URL, api_key=Config.TAUTULLI_API_KEY)
    
    # Get watched media history
    media_items = api.get_watched_media()
    
    # Create a dictionary of watched files with their last watch date
    watched_files = {}
    for item in media_items:
        if item.get('file'):
            # If we've seen this file before, only update if this watch is more recent
            if item['file'] not in watched_files or item['date'] > watched_files[item['file']]['date']:
                watched_files[item['file']] = {
                    'date': item['date'],
                    'title': item.get('full_title', 'Unknown Title')
                }
    
    # Process each file in the movies directory
    movies_dir = Config.MOVIES_DIR
    current_time = datetime.now()
    
    for filename in os.listdir(movies_dir):
        file_path = os.path.join(movies_dir, filename)
        
        if not os.path.isfile(file_path):
            continue
            
        # Check if this file has been watched
        watch_info = watched_files.get(file_path)
        
        if watch_info:
            # Condition 1: File has been watched AND it's been >= 30 days since watched
            days_since_watched = (current_time - datetime.fromtimestamp(watch_info['date'])).days
            if days_since_watched >= 30:
                try:
                    logger.info(f"Deleting watched file: {watch_info['title']} - Last watched: {days_since_watched} days ago")
                    os.remove(file_path)
                except OSError as e:
                    logger.error(f"Error deleting {file_path}: {e}")
        else:
            # Condition 2: File has not been watched AND it's been >= 180 days since adding the file
            file_stat = os.stat(file_path)
            days_since_added = (current_time - datetime.fromtimestamp(file_stat.st_mtime)).days
            if days_since_added >= 180:
                try:
                    logger.info(f"Deleting unwatched file: {filename} - Age: {days_since_added} days")
                    os.remove(file_path)
                except OSError as e:
                    logger.error(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    main()