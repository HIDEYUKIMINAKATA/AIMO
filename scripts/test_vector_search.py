# scripts/test_vector_search.py

import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from vector_index.search_index import search_similar_output

query = "ベクトル保存付きの入力と似ている文です。"

results = search_similar_output(query, top_k=3, threshold=0.8)

print("=== 検索結果 ===")
for r in results:
    print(f"スコア: {r['score']:.3f}")
    print(f"入力: {r['input_text']}")
    print(f"出力: {r['output_text']}")
    print("-" * 40)
