# scripts/test_saver_vec2.py

import os, sys
from sentence_transformers import SentenceTransformer

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from memory.cache.cache_hasher import generate_hash
from memory.cache.cache_saver import save_to_cache

MODEL = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

sample_input_text = "これはベクトルキャッシュのための別のテスト文です。"
sample_output_text = "この出力は2件目として保存されるものです。"
input_hash = generate_hash(sample_input_text)
vector = MODEL.encode(sample_input_text).tolist()

save_to_cache(
    input_hash=input_hash,
    input_text=sample_input_text,
    output_text=sample_output_text,
    model="mixtral-8x7b",
    tags=["test2"],
    vector=vector
)
