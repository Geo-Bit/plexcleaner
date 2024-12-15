import os
import logging
from datetime import datetime, timedelta
from tautulli_api import TautulliAPI
from config import Config
from logger import setup_logger

logger = setup_logger()

def main():
    # Call your API method to get watched media
    media_items = api.get_watched_media()
    
    # Ensure media_items is a list of dictionaries
    if not isinstance(media_items, list):
        print(f"Unexpected response format: {media_items}")
        return
    
    for item in media_items:
        if isinstance(item, dict):  # Verify each item is a dictionary
            file_path = item.get('file')  # Adjust key to match your actual needs
            if file_path:
                print(f"Processing file: {file_path}")
                # Add your processing logic here
            else:
                print(f"Missing 'file' key in item: {item}")
        else:
            print(f"Unexpected item format: {item}, Type: {type(item)}")


if __name__ == "__main__":
    main()
