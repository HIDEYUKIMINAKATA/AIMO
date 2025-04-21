import os
import sys
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ✅ AIMOパス解決
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
sys.path.insert(0, AIMO_ROOT)

from core.path_utils import find_aimo_root
from core.logger import log_event

AIMO_ROOT = find_aimo_root()
INDEX_FILE = os.path.join(AIMO_ROOT, "vector_index", "index_store.faiss")
ID_MAP_FILE = os.path.join(AIMO_ROOT, "vector_index", "id_map.json")
CACHE_FILE = os.path.join(AIMO_ROOT, "memory", "cache", "data", "cache_store.jsonl")

MODEL = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def get_recommended_outputs(input_text: str, top_k: int = 3, threshold: float = 0.4) -> list:
    """
    入力テキストに意味的に近いキャッシュ出力をFAISSからTop-Kで推薦する
    """
    try:
        input_vec = MODEL.encode(input_text).astype(np.float32).reshape(1, -1)
        input_vec = input_vec / np.linalg.norm(input_vec)

        if not os.path.exists(INDEX_FILE) or not os.path.exists(ID_MAP_FILE):
            log_event("FAISS index or ID map not found.", "ERROR")
            return []

        index = faiss.read_index(INDEX_FILE)
        with open(ID_MAP_FILE, "r", encoding="utf-8") as f:
            id_map = json.load(f)

        D, I = index.search(input_vec, top_k)
        results = []

        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache_lines = f.readlines()

        for score, idx in zip(D[0], I[0]):
            sim = 1 - score / 2  # cosine類似度近似
            if idx < 0 or sim < threshold:
                continue

            input_hash = id_map.get(str(idx))
            for line in cache_lines:
                try:
                    entry = json.loads(line)
                    if entry.get("input_hash") == input_hash:
                        results.append({
                            "score": round(sim, 4),
                            "input_hash": input_hash,
                            "input_text": entry.get("input_text", ""),
                            "output_text": entry.get("output_text", "")
                        })
                        break
                except Exception:
                    continue

        log_event(f"Recommended outputs found: {len(results)}", "SUCCESS")
        return results

    except Exception as e:
        log_event(f"semantic_recommender failed: {e}", "ERROR")
        return []
