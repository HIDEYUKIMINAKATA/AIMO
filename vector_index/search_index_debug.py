import os
import sys
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
AIMO_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, AIMO_ROOT)

from core.path_utils import find_aimo_root
from core.logger import log_event

AIMO_ROOT = find_aimo_root()
INDEX_FILE = os.path.join(AIMO_ROOT, "vector_index", "index_store.faiss")
ID_MAP_FILE = os.path.join(AIMO_ROOT, "vector_index", "id_map.json")
CACHE_FILE = os.path.join(AIMO_ROOT, "memory", "cache", "data", "cache_store.jsonl")

MODEL = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def search_similar_output_debug(input_text: str, top_k: int = 5, threshold: float = 0.0) -> list:
    try:
        if not os.path.exists(INDEX_FILE) or not os.path.exists(ID_MAP_FILE):
            log_event("FAISS index or ID map not found.", "ERROR")
            return []

        input_vector = MODEL.encode(input_text).astype(np.float32).reshape(1, -1)
        input_vector = input_vector / np.linalg.norm(input_vector)  # 正規化！

        index = faiss.read_index(INDEX_FILE)
        with open(ID_MAP_FILE, "r", encoding="utf-8") as f:
            id_map = json.load(f)

        D, I = index.search(input_vector, top_k)

        print("\n==== [DEBUG] FAISS Raw Output ====")
        for score, idx in zip(D[0], I[0]):
            approx_sim = 1 - score / 2
            print(f"idx: {idx}, L2距離: {score:.4f}, 類似度: {approx_sim:.4f}, 通過: {idx >= 0 and approx_sim >= threshold}")
        print("==================================\n")

        results = []
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache_lines = f.readlines()

        for score, idx in zip(D[0], I[0]):
            approx_sim = 1 - score / 2
            if idx >= 0 and approx_sim >= threshold:
                input_hash = id_map[idx]
                for line in cache_lines:
                    try:
                        entry = json.loads(line)
                        if entry.get("input_hash") == input_hash:
                            results.append({
                                "score": round(approx_sim, 4),
                                "input_text": entry.get("input_text"),
                                "output_text": entry.get("output_text"),
                                "input_hash": input_hash
                            })
                            break
                    except Exception:
                        continue

        if results:
            log_event(f"FAISS search hit {len(results)} entries.", "SUCCESS")
        else:
            log_event("FAISS search found no matching results.", "MISS")

        return results

    except Exception as e:
        log_event(f"FAISS search failed: {e}", "ERROR")
        return []
