# scripts/test_semantic.py

import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from memory.cache.semantic_search import find_semantically_similar

# 少し異なるけど意味が近いテキスト
test_input = "これは保存されたテスト入力の類似文です。"

result = find_semantically_similar(test_input)
print("SEMANTIC RESULT:", result)
