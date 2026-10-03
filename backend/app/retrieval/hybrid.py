from collections.abc import Sequence


class RRFFusion:
    def __init__(self, k: int = 60) -> None:
        if k < 1:
            raise ValueError("k must be at least 1")
        self.k = k

    def fuse(
        self,
        bm25_results: Sequence[dict[str, object]],
        vector_results: Sequence[dict[str, object]],
        top_k: int = 10,
    ) -> list[dict[str, object]]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1")

        fused: dict[str, dict[str, object]] = {}
        self._add_results(fused, bm25_results, "bm25")
        self._add_results(fused, vector_results, "vector")

        ranked = sorted(
            fused.values(),
            key=lambda result: result["rrf_score"],
            reverse=True,
        )[:top_k]
        return [
            {**result, "rank": rank}
            for rank, result in enumerate(ranked, start=1)
        ]

    def _add_results(
        self,
        fused: dict[str, dict[str, object]],
        results: Sequence[dict[str, object]],
        source: str,
    ) -> None:
        seen: set[str] = set()
        for position, result in enumerate(results, start=1):
            text = result.get("text")
            if not isinstance(text, str) or not text.strip() or text in seen:
                continue
            seen.add(text)
            contribution = 1 / (self.k + position)
            entry = fused.setdefault(
                text,
                {
                    "text": text,
                    "rrf_score": 0.0,
                    "sources": [],
                },
            )
            entry["rrf_score"] = float(entry["rrf_score"]) + contribution
            sources = entry["sources"]
            if isinstance(sources, list):
                sources.append(source)


def reciprocal_rank_fusion(
    bm25_results: Sequence[dict[str, object]],
    vector_results: Sequence[dict[str, object]],
    top_k: int = 10,
    k: int = 60,
) -> list[dict[str, object]]:
    return RRFFusion(k=k).fuse(bm25_results, vector_results, top_k=top_k)
