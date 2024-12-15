import os
import logging
from datetime import datetime, timedelta
from tautulli_api import TautulliAPI
from config import Config
from logger import setup_logger

logger = setup_logger()

def main():
    config = Config()
    api = TautulliAPI(config.tautulli_url, config.api_key)
    media_items = api.get_watched_media()
    now = datetime.now()

    for item in media_items:
        print(f"Item: {item}, Type: {type(item)}")
        file_path = item.get('file')
        if not file_path or config.tv_directory in file_path:
            continue

        last_watched = datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S')
        if item['watched_status'] == 1 and now - last_watched > timedelta(days=config.days_since_watched):
            os.remove(file_path)
            logger.info(f"Deleted watched file: {file_path}")

        elif item['watched_status'] == 0 and now - last_watched > timedelta(days=config.unwatched_cutoff):
            os.remove(file_path)
            logger.info(f"Deleted unwatched file: {file_path}")

if __name__ == "__main__":
    main()
