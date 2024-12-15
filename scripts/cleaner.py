import os
import logging
from datetime import datetime, timedelta
from tautulli_api import TautulliAPI
from config import Config
from logger import setup_logger

logger = setup_logger()

def process_movie_file(file_path, watched_files, current_time):
    """Process a single movie file and determine if it should be deleted"""
    # Check if this file has been watched
    watch_info = watched_files.get(file_path)
    logger.info(f"Watch info for {os.path.basename(file_path)}: {watch_info}")
    
    if watch_info:
        days_since_watched = (current_time - datetime.fromtimestamp(watch_info['date'])).days
        logger.info(f"File was watched {days_since_watched} days ago: {watch_info['title']}")
        
        if days_since_watched >= 30:
            try:
                logger.info(f"Deleting watched file: {watch_info['title']} - Last watched: {days_since_watched} days ago")
                os.remove(file_path)
                return True, 'watched'
            except OSError as e:
                logger.error(f"Error deleting {file_path}: {e}")
    else:
        file_stat = os.stat(file_path)
        days_since_added = (current_time - datetime.fromtimestamp(file_stat.st_mtime)).days
        logger.info(f"Unwatched file age: {days_since_added} days - {os.path.basename(file_path)}")
        
        if days_since_added >= 180:
            try:
                logger.info(f"Deleting unwatched file: {os.path.basename(file_path)} - Age: {days_since_added} days")
                os.remove(file_path)
                return True, 'unwatched'
            except OSError as e:
                logger.error(f"Error deleting {file_path}: {e}")
    
    return False, None

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
            if item['file'] not in watched_files or item['date'] > watched_files[item['file']]['date']:
                watched_files[item['file']] = {
                    'date': item['date'],
                    'title': item.get('full_title', 'Unknown Title')
                }
    
    logger.info(f"Found {len(watched_files)} unique watched files")
    
    # Process each file in the movies directory
    movies_dir = Config.MOVIES_DIR
    logger.info(f"Scanning directory: {movies_dir}")
    
    current_time = datetime.now()
    files_processed = 0
    files_to_delete_watched = 0
    files_to_delete_unwatched = 0
    
    # Walk through all directories
    for root, dirs, files in os.walk(movies_dir):
        for filename in files:
            # Only process video files
            if filename.endswith(('.mkv', '.mp4', '.avi')):
                file_path = os.path.join(root, filename)
                logger.info(f"Processing: {file_path}")
                
                files_processed += 1
                deleted, delete_type = process_movie_file(file_path, watched_files, current_time)
                
                if deleted:
                    if delete_type == 'watched':
                        files_to_delete_watched += 1
                    else:
                        files_to_delete_unwatched += 1

    # Log summary
    logger.info("=== Cleanup Summary ===")
    logger.info(f"Total files processed: {files_processed}")
    logger.info(f"Watched files deleted (≥30 days): {files_to_delete_watched}")
    logger.info(f"Unwatched files deleted (≥180 days): {files_to_delete_unwatched}")
    logger.info("=== End of Summary ===")

if __name__ == "__main__":
    main()