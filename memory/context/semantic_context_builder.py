import os
import sys
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ✅ AIMOパス解決
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.insert(0, AIMO_ROOT)

from core.path_utils import find_aimo_root
from core.logger import log_event

AIMO_ROOT = find_aimo_root()
INDEX_FILE = os.path.join(AIMO_ROOT, "vector_index", "index_store.faiss")
ID_MAP_FILE = os.path.join(AIMO_ROOT, "vector_index", "id_map.json")
CACHE_FILE = os.path.join(AIMO_ROOT, "memory", "cache", "data", "cache_store.jsonl")

MODEL = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def get_relevant_contexts(input_text: str, top_k: int = 3, threshold: float = 0.4) -> list:
    """
    FAISSインデックスから意味的に近い文脈を抽出（Top-K + 類似度スコア付き）
    """
    try:
        # ✅ 入力ベクトル生成＋正規化
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
            if idx < 0 or score > 2.0:
                continue

            sim = 1 - score / 2  # cosine類似度近似
            if sim < threshold:
                continue

            input_hash = id_map.get(str(idx))
            for line in cache_lines:
                try:
                    entry = json.loads(line)
                    if entry.get("input_hash") == input_hash:
                        results.append({
                            "score": round(sim, 4),
                            "source": entry.get("source", "cache"),
                            "text": entry.get("input_text") or entry.get("summary") or "[No Text]"
                        })
                        break
                except Exception:
                    continue

        log_event(f"Semantic context extracted (FAISS): {len(results)}", "SUCCESS")
        return results

    except Exception as e:
        log_event(f"FAISS semantic context search failed: {e}", "ERROR")
        return []
