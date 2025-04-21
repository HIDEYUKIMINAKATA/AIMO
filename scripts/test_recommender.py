import os
import sys

# ✅ AIMOルート解決
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from memory.cache.semantic_recommender import get_recommended_outputs

# 🧪 テスト用の入力
test_input = "自然エネルギーの将来性について教えてください。"

print("=== Semantic Recommender Test ===")

# ✅ 推薦候補を取得
results = get_recommended_outputs(test_input, top_k=5, threshold=0.3)

if not results:
    print("⚠️ 類似するキャッシュが見つかりませんでした。")
else:
    print(f"✅ {len(results)} 件の候補が見つかりました：\n")
    for i, r in enumerate(results, 1):
        print(f"--- Candidate #{i} ---")
        print(f"Score      : {r['score']}")
        print(f"Input Text : {r['input_text']}")
        print(f"Output Text: {r['output_text']}")
        print(f"Hash       : {r['input_hash']}")
        print()

print("=== End ===")
