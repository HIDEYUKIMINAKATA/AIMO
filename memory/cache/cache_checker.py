"""
cache_checker.py - AIMO memory/cache におけるキャッシュ判定モジュール

目的：
- 要約／出力の再生成を防ぐため、過去キャッシュを照合
- ハッシュまたは完全一致によるチェック機能を提供
"""

import hashlib
import json
from pathlib import Path
from core.logger import log_event
from core.find_aimo_root import find_aimo_root

CACHE_DIR = Path(find_aimo_root()) / "memory" / "cache"
CACHE_FILE = CACHE_DIR / "cache.jsonl"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

def load_cache() -> list:
    if not CACHE_FILE.exists():
        return []
    try:
        lines = CACHE_FILE.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines if line.strip()]
    except Exception as e:
        log_event("[ERROR]", f"キャッシュ読込失敗: {e}", category="cache")
        return []

def is_prompt_cached(prompt: str) -> bool:
    hash_key = _hash_prompt(prompt)
    cache = load_cache()
    for entry in cache:
        if entry.get("hash") == hash_key:
            log_event("[INFO]", "キャッシュ一致: 再生成をスキップ", category="cache")
            return True
    return False

def add_prompt_to_cache(prompt: str):
    hash_key = _hash_prompt(prompt)
    entry = {"hash": hash_key, "prompt": prompt}
    try:
        with open(CACHE_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        log_event("[SUCCESS]", "キャッシュに追加完了", category="cache")
    except Exception as e:
        log_event("[ERROR]", f"キャッシュ保存失敗: {e}", category="cache")

# CLI用テスト
if __name__ == "__main__":
    test_prompt = "これはテストプロンプトです。"
    if is_prompt_cached(test_prompt):
        print("[INFO] キャッシュ済みのプロンプトです。")
    else:
        add_prompt_to_cache(test_prompt)
        print("[INFO] 新規キャッシュに追加しました。")
