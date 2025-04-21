import os
import json
from datetime import datetime

from core.path_utils import find_aimo_root
from core.logger import log_event

AIMO_ROOT = find_aimo_root()
CACHE_DIR = os.path.join(AIMO_ROOT, "memory", "cache", "data")
CACHE_FILE = os.path.join(CACHE_DIR, "cache_store.jsonl")

# 保存先ディレクトリを保証
os.makedirs(CACHE_DIR, exist_ok=True)

def save_to_cache(input_hash: str, input_text: str, output_text: str,
                  model: str = "unknown", tags: list = None, vector=None) -> None:
    try:
        if tags is None:
            tags = []

        # 重複チェック
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if entry.get("input_hash") == input_hash:
                            log_event(f"Cache already exists for hash: {input_hash}", "SKIP")
                            return
                    except json.JSONDecodeError:
                        continue

        # 保存するデータ構造
        data = {
            "input_hash": input_hash,
            "input_text": input_text,
            "output_text": output_text,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model": model,
            "tags": tags,
            "vector": vector if vector else None  # ← ベクトル保存対応！
        }

        with open(CACHE_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

        log_event(f"Cache saved for hash: {input_hash}", "SUCCESS")

    except Exception as e:
        log_event(f"Cache saving failed: {e}", "ERROR")
