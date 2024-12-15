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
    
    logger.info("Starting media cleanup process...")
    
    # Get watched media history
    media_items = api.get_watched_media()
    logger.info(f"Retrieved {len(media_items)} items from watch history")
    
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
    
    logger.info(f"Found {len(watched_files)} unique watched files")
    
    # Process each file in the movies directory
    movies_dir = Config.MOVIES_DIR
    logger.info(f"Scanning directory: {movies_dir}")
    
    try:
        files = os.listdir(movies_dir)
        logger.info(f"Found {len(files)} items in movies directory")
        logger.debug("Directory contents:")
        for f in files:
            logger.debug(f"  - {f}")
    except Exception as e:
        logger.error(f"Error listing directory contents: {e}")
    
    current_time = datetime.now()
    files_processed = 0
    files_to_delete_watched = 0
    files_to_delete_unwatched = 0
    
    for filename in os.listdir(movies_dir):
        file_path = os.path.join(movies_dir, filename)
        logger.debug(f"Checking path: {file_path}")
        
        if not os.path.isfile(file_path):
            logger.debug(f"Skipping non-file: {filename}")
            continue
            
        files_processed += 1
        logger.debug(f"Processing file: {filename}")
            
        # Check if this file has been watched
        watch_info = watched_files.get(file_path)
        logger.debug(f"Watch info for {filename}: {watch_info}")
        
        if watch_info:
            # Condition 1: File has been watched AND it's been >= 30 days since watched
            days_since_watched = (current_time - datetime.fromtimestamp(watch_info['date'])).days
            logger.debug(f"File was watched {days_since_watched} days ago: {watch_info['title']}")
            
            if days_since_watched >= 30:
                files_to_delete_watched += 1
                try:
                    logger.info(f"Deleting watched file: {watch_info['title']} - Last watched: {days_since_watched} days ago")
                    os.remove(file_path)
                except OSError as e:
                    logger.error(f"Error deleting {file_path}: {e}")
        else:
            # Condition 2: File has not been watched AND it's been >= 180 days since adding the file
            file_stat = os.stat(file_path)
            days_since_added = (current_time - datetime.fromtimestamp(file_stat.st_mtime)).days
            logger.debug(f"Unwatched file age: {days_since_added} days - {filename}")
            
            if days_since_added >= 180:
                files_to_delete_unwatched += 1
                try:
                    logger.info(f"Deleting unwatched file: {filename} - Age: {days_since_added} days")
                    os.remove(file_path)
                except OSError as e:
                    logger.error(f"Error deleting {file_path}: {e}")

    # Log summary
    logger.info("=== Cleanup Summary ===")
    logger.info(f"Total files processed: {files_processed}")
    logger.info(f"Watched files deleted (≥30 days): {files_to_delete_watched}")
    logger.info(f"Unwatched files deleted (≥180 days): {files_to_delete_unwatched}")
    logger.info("=== End of Summary ===")

if __name__ == "__main__":
    main()