"""vector_memory.py – S4: FAISS + sentence-transformers based semantic memory

Responsibilities
----------------
• Build or load a FAISS index for embeddings
• Provide `add_memory(text)` and `search_memory(query, top_k=5)` APIs
• Persist memories to `memory/memory_vector.json`
• All actions are logged via core.logger.log_event
"""

import os
import json
from pathlib import Path
from typing import List, Tuple

import faiss
from sentence_transformers import SentenceTransformer

from core.logger import log_event
from core.find_aimo_root import find_aimo_root

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMB_DIM = 384

class VectorMemory:
    def __init__(self):
        self.root = Path(find_aimo_root())
        self.mem_file = self.root / "memory" / "memory_vector.json"
        self.index_file = self.root / "memory" / "memory_vector.index"

        try:
            self.model = SentenceTransformer(MODEL_NAME)
            log_event("[INFO]", f"SentenceTransformer model loaded: {MODEL_NAME}")
        except Exception as e:
            log_event("[ERROR]", f"Failed to load transformer model: {e}")
            raise

        self._init_index()
        self._load_vectors()

    def _init_index(self):
        if self.index_file.exists():
            try:
                self.index = faiss.read_index(str(self.index_file))
                log_event("[INFO]", "FAISS index loaded")
            except Exception as e:
                log_event("[ERROR]", f"Failed to load FAISS index: {e}")
                self.index = faiss.IndexFlatL2(EMB_DIM)
                log_event("[WARN]", "Initialized new FAISS index instead")
        else:
            self.index = faiss.IndexFlatL2(EMB_DIM)
            log_event("[INFO]", "FAISS index created")

    def _load_vectors(self):
        if self.mem_file.exists():
            try:
                with open(self.mem_file, "r", encoding="utf-8") as f:
                    self.mem_data = json.load(f)
                log_event("[INFO]", f"Loaded {len(self.mem_data)} vector memories")
            except Exception as e:
                self.mem_data = []
                log_event("[ERROR]", f"Failed to load memory_vector.json: {e}")
        else:
            self.mem_data = []
            log_event("[INFO]", "No previous memory found, starting fresh")

    def _save(self):
        try:
            with open(self.mem_file, "w", encoding="utf-8") as f:
                json.dump(self.mem_data, f, ensure_ascii=False, indent=2)
            faiss.write_index(self.index, str(self.index_file))
            log_event("[SUCCESS]", f"Vector memory persisted to disk (total: {len(self.mem_data)})")
        except Exception as e:
            log_event("[ERROR]", f"Failed to persist vector memory: {e}")

    def add_memory(self, text: str) -> None:
        try:
            vec = self.model.encode([text])
            self.index.add(vec)
            self.mem_data.append(text)
            log_event("[INFO]", f"Memory added: {text[:50]}…")
            self._save()
        except Exception as e:
            log_event("[ERROR]", f"Failed to add memory: {e}")

    def search_memory(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        try:
            q_vec = self.model.encode([query])
            D, I = self.index.search(q_vec, top_k)
            results = []
            for idx, dist in zip(I[0], D[0]):
                if idx == -1:
                    continue
                results.append((self.mem_data[idx], float(dist)))
            log_event("[INFO]", f"Memory search completed for query: {query} (top_k={top_k})")
            return results
        except Exception as e:
            log_event("[ERROR]", f"Memory search failed: {e}")
            return []
