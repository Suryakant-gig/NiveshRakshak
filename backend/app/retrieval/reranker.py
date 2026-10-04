import math
from collections.abc import Sequence

from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        max_length: int = 512,
    ) -> None:
        if max_length < 1:
            raise ValueError("max_length must be at least 1")
        self.model = CrossEncoder(model_name, max_length=max_length)

    def rerank(
        self,
        claim: str,
        evidence: Sequence[dict[str, object]],
        top_k: int = 10,
    ) -> list[dict[str, object]]:
        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("claim must be a non-empty string")
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        if not evidence:
            return []

        pairs: list[list[str]] = []
        valid_evidence: list[dict[str, object]] = []
        for item in evidence:
            text = item.get("text")
            if not isinstance(text, str) or not text.strip():
                raise ValueError("each evidence item must contain non-empty text")
            pairs.append([claim, text])
            valid_evidence.append(item)

        scores = self.model.predict(pairs)
        ranked = []
        for item, score in zip(valid_evidence, scores):
            result = dict(item)
            raw_score = float(score)
            result["reranker_score"] = raw_score
            if raw_score >= 0:
                relevance_score = 1 / (1 + math.exp(-raw_score))
            else:
                exp_score = math.exp(raw_score)
                relevance_score = exp_score / (1 + exp_score)
            result["relevance_score"] = relevance_score
            ranked.append(result)

        ranked.sort(key=lambda result: result["reranker_score"], reverse=True)
        return [
            {**result, "rank": rank}
            for rank, result in enumerate(ranked[:top_k], start=1)
        ]
