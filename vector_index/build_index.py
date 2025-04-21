import os
import sys
import json
import faiss
import numpy as np
from sklearn.preprocessing import normalize

# ✅ AIMOルート追加
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from core.path_utils import find_aimo_root
from core.logger import log_event

AIMO_ROOT = find_aimo_root()
CACHE_FILE = os.path.join(AIMO_ROOT, "memory", "cache", "data", "cache_store.jsonl")
INDEX_FILE = os.path.join(AIMO_ROOT, "vector_index", "index_store.faiss")
ID_MAP_FILE = os.path.join(AIMO_ROOT, "vector_index", "id_map.json")

os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)

def build_faiss_index():
    try:
        if not os.path.exists(CACHE_FILE):
            log_event("Cache file not found. Cannot build FAISS index.", "ERROR")
            return

        vectors = []
        id_map = []
        
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    vector = entry.get("vector", None)
                    input_hash = entry.get("input_hash", None)

                    if vector and input_hash and isinstance(vector, list):
                        vectors.append(np.array(vector, dtype=np.float32))
                        id_map.append(input_hash)
                except Exception:
                    continue

        if not vectors:
            log_event("No valid vectors found in cache. Index not built.", "WARN")
            return

        mat = np.vstack(vectors).astype(np.float32)
        mat = normalize(mat, norm='l2')  # ✅ 正規化
        index = faiss.IndexFlatL2(mat.shape[1])
        index.add(mat)

        faiss.write_index(index, INDEX_FILE)
        with open(ID_MAP_FILE, "w", encoding="utf-8") as f:
            json.dump(id_map, f, ensure_ascii=False, indent=2)

        log_event(f"FAISS index built and saved with {len(id_map)} vectors.", "SUCCESS")

    except Exception as e:
        log_event(f"FAISS index build failed: {e}", "ERROR")

if __name__ == "__main__":
    build_faiss_index()
