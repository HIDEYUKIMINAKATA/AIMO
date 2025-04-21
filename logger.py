# logger.py
from datetime import datetime
import os

def log_event(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{level} {timestamp} {message}")
