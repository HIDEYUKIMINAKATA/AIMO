import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from vector_index.search_index_debug import search_similar_output_debug

query = "これは意味的検索のテストです。"
results = search_similar_output_debug(query, top_k=5, threshold=0.0)

print("=== 検索結果 ===")
for r in results:
    print(f"Score: {r['score']} | Hash: {r['input_hash']}")
    print(f"Input: {r['input_text']}")
    print(f"Output: {r['output_text']}")
    print("-" * 30)
