# Semantic embedding and vector search
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class SemanticSearch:
    def __init__(self, chunks, model_name=MODEL_NAME):
        self.chunks = chunks
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.embeddings = None
        self._build_index()

    def _build_index(self):
        texts = [chunk["text"] for chunk in self.chunks]

        if not texts:
            self.embeddings = np.empty((0, 384), dtype="float32")
            return

        self.embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype("float32")

        self.index = faiss.IndexFlatIP(self.embeddings.shape[1])
        self.index.add(self.embeddings)

    def search(self, query, top_k=10):
        if self.index is None or not self.chunks:
            return []

        k = min(top_k, len(self.chunks))

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype("float32")

        scores, indices = self.index.search(query_embedding, k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue

            result = dict(self.chunks[int(index)])
            result["semantic_score"] = float(score)
            results.append(result)

        return results
