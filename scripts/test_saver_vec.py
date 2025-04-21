import sys
import os
from sentence_transformers import SentenceTransformer

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from memory.cache.cache_hasher import generate_hash
from memory.cache.cache_saver import save_to_cache

MODEL = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

sample_input_text = "これはベクトル保存付きのテスト入力です。"
sample_output_text = "ベクトル保存と意味検索に使う出力です。"
model_name = "mixtral-8x7b"
tags = ["test", "vector"]

# ベクトル事前生成
vector = MODEL.encode(sample_input_text).tolist()

input_hash = generate_hash(sample_input_text)

save_to_cache(
    input_hash=input_hash,
    input_text=sample_input_text,
    output_text=sample_output_text,
    model=model_name,
    tags=tags,
    vector=vector  # ✅ 保存
)
