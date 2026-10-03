import re
from collections.abc import Sequence
from urllib.parse import urlparse


class ClaimSourceSearch:
    _url_pattern = re.compile(r"https?://[^\s<>()\[\]{}\"']+")
    _token_pattern = re.compile(r"[a-z0-9]+%?", re.IGNORECASE)
    _official_domains = {
        "rbi.org.in",
        "sebi.gov.in",
        "sec.gov",
        "ftc.gov",
        "fca.org.uk",
        "cftc.gov",
    }

    def search(
        self,
        claim: str | dict[str, object],
        candidates: Sequence[dict[str, object]],
        top_k: int = 10,
    ) -> dict[str, object]:
        claim_id = None
        if isinstance(claim, dict):
            claim_id = claim.get("id")
            claim_text = claim.get("text")
        else:
            claim_text = claim

        if not isinstance(claim_text, str) or not claim_text.strip():
            raise ValueError("claim must contain non-empty text")
        if top_k < 1:
            raise ValueError("top_k must be at least 1")

        claim_tokens = set(self._tokenize(claim_text))
        evidence = [
            self._annotate_candidate(candidate, claim_tokens, position)
            for position, candidate in enumerate(candidates, start=1)
        ]
        evidence.sort(
            key=lambda item: (
                float(item["relevance_score"]),
                float(item["source_match_score"]),
                float(item["source_quality"]),
            ),
            reverse=True,
        )
        evidence = [
            {**item, "rank": rank}
            for rank, item in enumerate(evidence[:top_k], start=1)
        ]

        result: dict[str, object] = {
            "claim": claim_text,
            "evidence": evidence,
        }
        if claim_id is not None:
            result["claim_id"] = claim_id
        return result

    def _annotate_candidate(
        self,
        candidate: dict[str, object],
        claim_tokens: set[str],
        position: int,
    ) -> dict[str, object]:
        text = candidate.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("each candidate must contain non-empty text")

        result = dict(candidate)
        url = candidate.get("url")
        if not isinstance(url, str) or not url.strip():
            url = self.extract_url(text)
        if url:
            result["url"] = url

        source = candidate.get("source")
        if not isinstance(source, str) or not source.strip():
            source = self.source_from_url(url)
        result["source"] = source or "unknown"
        result["source_type"] = self.classify_source(url, text)
        result["channel"] = self.classify_channel(url, text)

        candidate_tokens = set(self._tokenize(text))
        overlap = claim_tokens.intersection(candidate_tokens)
        result["source_match_score"] = len(overlap) / max(len(claim_tokens), 1)
        result["matched_terms"] = sorted(overlap)
        result["source_quality"] = self.source_quality(
            result["source_type"],
            result["source"],
        )
        result["relevance_score"] = self._existing_score(candidate, position)
        return result

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return [token.lower() for token in ClaimSourceSearch._token_pattern.findall(text)]

    @staticmethod
    def _existing_score(candidate: dict[str, object], position: int) -> float:
        for field in ("relevance_score", "reranker_score", "rrf_score", "score"):
            value = candidate.get(field)
            if isinstance(value, int | float):
                return float(value)
        return 1 / position

    @classmethod
    def extract_url(cls, text: str) -> str | None:
        match = cls._url_pattern.search(text)
        return match.group(0).rstrip(".,;:!?)]}") if match else None

    @classmethod
    def source_from_url(cls, url: str | None) -> str | None:
        if not url:
            return None
        host = urlparse(url).netloc.lower().removeprefix("www.")
        return host or None

    @classmethod
    def classify_source(cls, url: str | None, text: str) -> str:
        host = cls.source_from_url(url)
        if host and any(host == domain or host.endswith(f".{domain}") for domain in cls._official_domains):
            return "official_regulator"
        if host:
            return "web_source"
        lowered = text.lower()
        if any(term in lowered for term in ("bank", "rbi", "sebi", "regulator")):
            return "financial_or_regulatory_reference"
        return "unknown"

    @staticmethod
    def source_quality(source_type: object, source: object) -> float:
        if source_type == "official_regulator":
            return 1.0
        if source_type == "financial_or_regulatory_reference":
            return 0.75
        if source_type == "web_source":
            return 0.5
        if isinstance(source, str) and source.strip() and source != "unknown":
            return 0.35
        return 0.1

    @staticmethod
    def classify_channel(url: str | None, text: str) -> str:
        if url:
            return "web"
        lowered = text.lower()
        if any(term in lowered for term in ("sms", "text message", "whatsapp", "telegram")):
            return "messaging"
        if "email" in lowered or "inbox" in lowered:
            return "email"
        if any(term in lowered for term in ("call", "caller", "phone number")):
            return "phone"
        return "unknown"
