import sys
import os

# AIMOルートの動的検出
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from memory.cache.cache_hasher import generate_hash
from memory.cache.cache_saver import save_to_cache

# テスト用入力と出力
sample_input_text = "これはテスト入力です。"
sample_output_text = "これはテストの結果として保存される出力です。"
model_name = "mixtral-8x7b"
tags = ["test", "saver", "cache"]

# ハッシュ生成
input_hash = generate_hash(sample_input_text)

# キャッシュ保存実行
save_to_cache(
    input_hash=input_hash,
    input_text=sample_input_text,
    output_text=sample_output_text,
    model=model_name,
    tags=tags
)
