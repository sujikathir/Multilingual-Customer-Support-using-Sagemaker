# File: multilingual-support/logger.py

import logging
import sys
from pathlib import Path

# Define logging config here instead of importing from config
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_path': 'logs/application.log'
}

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger with the specified configuration
    
    Args:
        name (str): Name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_CONFIG['level'])

    # Create formatter
    formatter = logging.Formatter(LOGGING_CONFIG['format'])

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler
    log_file_path = Path(LOGGING_CONFIG['file_path'])
    log_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger