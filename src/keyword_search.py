# Keyword search using BM25
import re
from rank_bm25 import BM25Okapi


class KeywordSearch:
    def __init__(self, chunks):
        self.chunks = chunks

        self.tokenized_documents = [
            self._tokenize(chunk["text"])
            for chunk in chunks
        ]

        self.bm25 = (
            BM25Okapi(self.tokenized_documents)
            if self.tokenized_documents
            else None
        )

    @staticmethod
    def _tokenize(text):
        return re.findall(
            r"[A-Za-z0-9]+",
            text.lower()
        )

    def search(self, query, top_k=10):
        if self.bm25 is None:
            return []

        query_tokens = self._tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        results = []

        for index in ranked_indices[
            :min(top_k, len(ranked_indices))
        ]:
            result = dict(self.chunks[index])

            result["keyword_score"] = float(
                scores[index]
            )

            results.append(result)

        return results
