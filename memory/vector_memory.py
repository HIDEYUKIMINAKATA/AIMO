# memory/vector_memory.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from core.logger import log_event

class VectorMemory:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(384)  # 384次元ベクトル
        self.text_store: List[str] = []

    def add(self, text: str):
        emb = self.model.encode([text])
        self.index.add(np.array(emb, dtype="float32"))
        self.text_store.append(text)
        log_event("INFO", f"記憶追加：{text[:30]}...")

    def similar(self, query: str, k=3) -> List[str]:
        if len(self.text_store) == 0:
            log_event("WARN", "記憶が空です")
            return []

        emb = self.model.encode([query])
        D, I = self.index.search(np.array(emb, dtype="float32"), k)
        results = [self.text_store[i] for i in I[0] if i < len(self.text_store)]
        log_event("INFO", f"類似検索クエリ：{query[:30]}...")
        return results
