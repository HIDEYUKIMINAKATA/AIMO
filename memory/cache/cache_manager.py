import os
import sys

# ✅ AIMOルート解決（実行ファイルから）
AIMO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, AIMO_ROOT)

from core.path_utils import find_aimo_root
from core.logger import log_event
from memory.cache.cache_hasher import generate_hash
from memory.cache.cache_loader import load_from_cache
from memory.cache.cache_saver import save_to_cache
from memory.cache.semantic_search import search_similar_output

AIMO_ROOT = find_aimo_root()

def process_input_with_cache(input_text: str, top_k: int = 3, threshold: float = 0.6) -> dict:
    try:
        log_event("=== AIMO Cache Manager Start ===", "INFO")
        input_hash = generate_hash(input_text)

        # ✅ 1. ハッシュ一致検索
        cached = load_from_cache(input_hash)
        if cached:
            log_event("Cache HIT by HASH", "SUCCESS")
            return {
                "status": "hash_hit",
                "output": cached.get("output_text"),
                "input": cached.get("input_text"),
                "input_hash": input_hash,
                "similar": []
            }

        # ✅ 2. 意味的一致検索（FAISS）
        similar_results = search_similar_output(input_text, top_k=top_k, threshold=threshold)
        if similar_results:
            log_event("Cache HIT by SEMANTIC MATCH", "SUCCESS")
            return {
                "status": "semantic_hit",
                "output": None,
                "input": input_text,
                "input_hash": input_hash,
                "similar": similar_results
            }

        # ✅ 3. キャッシュ未命中 → AI出力（ここではスタブ）
        dummy_output = "【STUB】これはAIが生成した出力です（実際のAPI未連携）"
        save_to_cache(input_text, dummy_output)
        log_event("AI Output Saved to Cache (STUB)", "SUCCESS")

        return {
            "status": "generated",
            "output": dummy_output,
            "input": input_text,
            "input_hash": input_hash,
            "similar": []
        }

    except Exception as e:
        log_event(f"Cache Manager failed: {e}", "ERROR")
        return {
            "status": "error",
            "error": str(e),
            "input": input_text,
            "input_hash": None,
            "similar": []
        }
