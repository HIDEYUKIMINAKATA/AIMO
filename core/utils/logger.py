# core/logger.py

import os
from datetime import datetime
from core.find_aimo_root import find_aimo_root

ROOT = find_aimo_root()
LOG_DIR = os.path.join(ROOT, "logs")

def log_event(level: str, message: str, category: str = "system"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{level} {now} | {message}"

    print(line)

    # ログファイル保存
    cat_dir = os.path.join(LOG_DIR, category)
    os.makedirs(cat_dir, exist_ok=True)
    file_path = os.path.join(cat_dir, f"{datetime.now().strftime('%Y%m%d')}.log")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
