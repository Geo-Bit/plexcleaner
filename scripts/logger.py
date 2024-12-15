import logging

def setup_logger():
    # Create logger
    logger = logging.getLogger('plex-cleaner')
    logger.setLevel(logging.DEBUG)  # Set to DEBUG level
    
    # Create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Add formatter to ch
    ch.setFormatter(formatter)
    
    # Add ch to logger
    logger.addHandler(ch)
    
    return logger
