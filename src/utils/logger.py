import logging
import os
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_format = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, "bot.log"),
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
console_handler.setLevel(logging.INFO)

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger
