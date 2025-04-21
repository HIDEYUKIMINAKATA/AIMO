import os
import sys

# ✅ AIMOルートをパスに追加（重要！）
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from memory.cache.cache_manager import process_input_with_cache

query = "これは意味キャッシュ統合のテストです。"

result = process_input_with_cache(query, top_k=5, threshold=0.4)

print("\n=== 結果 ===")
print(f"Status: {result['status']}")
print(f"Input: {result['input']}")
print(f"Hash: {result['input_hash']}")
print(f"Output: {result['output']}")
print(f"類似候補数: {len(result['similar'])}")
if result["similar"]:
    for s in result["similar"]:
        print(f"- Score: {s['score']:.4f} / Input: {s['input_text']}")
