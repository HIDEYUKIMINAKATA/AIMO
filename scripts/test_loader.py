import sys
import os

# AIMOルートを動的に追加
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from memory.cache.cache_hasher import generate_hash
from memory.cache.cache_loader import load_from_cache

# テスト用入力（test_saver.py で使ったものと同じ）
sample_input_text = "これはテスト入力です。"

# ハッシュ生成
input_hash = generate_hash(sample_input_text)

# ロード試行
cached_output = load_from_cache(input_hash)

print("CACHED OUTPUT:", cached_output)
