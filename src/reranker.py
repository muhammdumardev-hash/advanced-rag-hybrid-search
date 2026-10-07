# Cross-encoder reranking
from sentence_transformers import CrossEncoder

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"


class Reranker:
    def __init__(self, model_name=MODEL_NAME):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, candidates, top_k=3):
        if not candidates:
            return []

        pairs = [
            (query, candidate["text"])
            for candidate in candidates
        ]

        scores = self.model.predict(
            pairs,
            show_progress_bar=False
        )

        results = []

        for candidate, score in zip(candidates, scores):
            result = dict(candidate)
            result["rerank_score"] = float(score)
            results.append(result)

        results.sort(
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        return results[:min(top_k, len(results))]
