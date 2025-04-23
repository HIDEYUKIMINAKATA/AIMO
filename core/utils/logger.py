# core/utils/logger.py
from datetime import datetime
import inspect
from pathlib import Path

def log_event(level: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    caller = inspect.stack()[1]
    origin = Path(caller.filename).name
    print(f"{message} {timestamp} | {level} ({origin})")
