# Hybrid semantic + keyword retrieval
def _normalize_scores(results, score_key):
    if not results:
        return {}

    values = [
        float(item.get(score_key, 0.0))
        for item in results
    ]

    low = min(values)
    high = max(values)

    if high == low:
        return {
            item["chunk_id"]: (
                1.0 if high > 0 else 0.0
            )
            for item in results
        }

    return {
        item["chunk_id"]: (
            float(item.get(score_key, 0.0)) - low
        ) / (high - low)
        for item in results
    }


def hybrid_search(
    semantic_results,
    keyword_results,
    top_k=10,
    semantic_weight=0.60,
    keyword_weight=0.40,
):
    """
    Combine semantic and BM25 keyword search
    using normalized weighted scores.
    """

    total = semantic_weight + keyword_weight

    if total <= 0:
        semantic_weight = 0.5
        keyword_weight = 0.5
    else:
        semantic_weight /= total
        keyword_weight /= total

    semantic_scores = _normalize_scores(
        semantic_results,
        "semantic_score"
    )

    keyword_scores = _normalize_scores(
        keyword_results,
        "keyword_score"
    )

    combined = {}

    for result in semantic_results:
        combined.setdefault(
            result["chunk_id"],
            dict(result)
        )

    for result in keyword_results:
        combined.setdefault(
            result["chunk_id"],
            dict(result)
        )

    ranked = []

    for chunk_id, result in combined.items():

        result["semantic_score"] = float(
            result.get("semantic_score", 0.0)
        )

        result["keyword_score"] = float(
            result.get("keyword_score", 0.0)
        )

        result["hybrid_score"] = (
            semantic_weight
            * semantic_scores.get(chunk_id, 0.0)
            +
            keyword_weight
            * keyword_scores.get(chunk_id, 0.0)
        )

        ranked.append(result)

    ranked.sort(
        key=lambda item: item["hybrid_score"],
        reverse=True
    )

    return ranked[:top_k]
