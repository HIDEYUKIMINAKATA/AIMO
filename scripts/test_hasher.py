# scripts/test_hasher.py

import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from memory.cache.cache_hasher import generate_hash

sample_input = {
    "text": "これはテスト入力です。",
    "lang": "ja"
}

hash_result = generate_hash(sample_input)
print("HASH:", hash_result)
