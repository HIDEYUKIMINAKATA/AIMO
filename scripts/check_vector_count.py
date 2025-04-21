# scripts/check_vector_count.py

import os
import json

path = "memory/cache/data/cache_store.jsonl"
count = 0

with open(path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            if "vector" in data and isinstance(data["vector"], list):
                count += 1
        except:
            continue

print(f"[CHECK] ベクトル付きエントリ数: {count}")
