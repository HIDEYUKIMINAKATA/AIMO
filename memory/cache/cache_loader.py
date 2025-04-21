import os
import json

from core.path_utils import find_aimo_root
from core.logger import log_event

AIMO_ROOT = find_aimo_root()
CACHE_FILE = os.path.join(AIMO_ROOT, "memory", "cache", "data", "cache_store.jsonl")

def load_from_cache(input_hash: str) -> str | None:
    try:
        if not os.path.exists(CACHE_FILE):
            log_event("Cache file not found. Skipping lookup.", "WARN")
            return None

        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("input_hash") == input_hash:
                        log_event(f"Cache HIT for hash: {input_hash}", "HIT")
                        return entry.get("output_text", None)
                except json.JSONDecodeError:
                    continue  # 不正行はスキップ

        log_event(f"Cache MISS for hash: {input_hash}", "MISS")
        return None

    except Exception as e:
        log_event(f"Cache load failed: {e}", "ERROR")
        return None
