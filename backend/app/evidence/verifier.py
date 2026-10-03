import re
from collections.abc import Sequence


class ClaimVerifier:
    STATUSES = {
        "SUPPORTED",
        "CONTRADICTED",
        "UNSUPPORTED",
        "UNVERIFIED",
    }
    _token_pattern = re.compile(r"[a-z0-9]+%?", re.IGNORECASE)
    _negation_terms = {
        "cannot",
        "can't",
        "no",
        "not",
        "never",
        "without",
        "prohibited",
        "illegal",
        "false",
        "invalid",
        "deny",
        "denied",
    }
    _negative_claim_terms = {
        "scam",
        "scams",
        "fraud",
        "fraudulent",
        "phishing",
        "deceptive",
        "illegal",
        "fake",
        "warning",
        "warnings",
    }
    _stop_words = {
        "about",
        "after",
        "again",
        "also",
        "and",
        "are",
        "been",
        "being",
        "from",
        "have",
        "into",
        "that",
        "their",
        "there",
        "these",
        "they",
        "this",
        "through",
        "with",
        "would",
    }

    def verify(
        self,
        claim: dict[str, object],
        evidence: Sequence[dict[str, object]],
    ) -> dict[str, object]:
        claim_id = claim.get("id")
        claim_text = claim.get("text")
        if not isinstance(claim_id, str) or not claim_id.strip():
            raise ValueError("claim must contain a non-empty id")
        if not isinstance(claim_text, str) or not claim_text.strip():
            raise ValueError("claim must contain non-empty text")

        normalized_evidence = self._normalize_evidence(evidence)
        status = self._determine_status(claim_text, normalized_evidence)
        return {
            "claim_id": claim_id,
            "status": status,
            "evidence": normalized_evidence,
        }

    def verify_claim(
        self,
        claim: dict[str, object],
        evidence: Sequence[dict[str, object]],
    ) -> dict[str, object]:
        return self.verify(claim, evidence)

    def _normalize_evidence(
        self,
        evidence: Sequence[dict[str, object]],
    ) -> list[dict[str, object]]:
        normalized = []
        for item in evidence:
            text = item.get("text")
            if not isinstance(text, str) or not text.strip():
                continue
            source = item.get("source", "unknown")
            if not isinstance(source, str) or not source.strip():
                source = "unknown"
            normalized.append(
                {
                    "source": source,
                    "text": text,
                    "relevance_score": self._score(item),
                }
            )
        normalized.sort(key=lambda item: item["relevance_score"], reverse=True)
        return normalized

    @staticmethod
    def _score(item: dict[str, object]) -> float:
        for field in ("relevance_score", "reranker_score", "rrf_score", "score"):
            value = item.get(field)
            if isinstance(value, int | float):
                return float(value)
        return 0.0

    def _determine_status(
        self,
        claim: str,
        evidence: Sequence[dict[str, object]],
    ) -> str:
        if not evidence:
            return "UNVERIFIED"

        claim_terms = self._meaningful_terms(claim)
        claim_numbers = self._number_terms(claim)
        claim_polarity = self._polarity(claim)
        relevant = []
        supporting = []
        contradicting = []

        for item in evidence:
            evidence_text = str(item["text"])
            evidence_terms = self._meaningful_terms(evidence_text)
            overlap = len(claim_terms.intersection(evidence_terms)) / max(len(claim_terms), 1)
            if overlap < 0.25:
                continue
            relevant.append(item)
            if claim_numbers and not claim_numbers.issubset(self._number_terms(evidence_text)):
                continue

            evidence_polarity = self._polarity(evidence_text)
            if evidence_polarity == claim_polarity and overlap >= 0.4:
                supporting.append(item)
            elif evidence_polarity != claim_polarity:
                contradicting.append(item)

        if supporting and contradicting:
            best_support = max(supporting, key=self._score)
            best_contradiction = max(contradicting, key=self._score)
            return (
                "SUPPORTED"
                if self._score(best_support) >= self._score(best_contradiction)
                else "CONTRADICTED"
            )
        if supporting:
            return "SUPPORTED"
        if contradicting:
            return "CONTRADICTED"
        if relevant:
            return "UNSUPPORTED"
        return "UNVERIFIED"

    def _polarity(self, text: str) -> int:
        tokens = set(self._tokens(text))
        has_negation = bool(tokens.intersection(self._negation_terms))
        has_negative_claim = bool(tokens.intersection(self._negative_claim_terms))
        return -1 if has_negation or has_negative_claim else 1

    def _meaningful_terms(self, text: str) -> set[str]:
        return {
            self._stem(token)
            for token in self._tokens(text)
            if len(token) >= 3 and token not in self._stop_words
        }

    def _number_terms(self, text: str) -> set[str]:
        return {token for token in self._tokens(text) if any(char.isdigit() for char in token)}

    def _tokens(self, text: str) -> list[str]:
        return [token.lower() for token in self._token_pattern.findall(text)]

    @staticmethod
    def _stem(token: str) -> str:
        for suffix in ("ing", "ed", "es", "s"):
            if token.endswith(suffix) and len(token) - len(suffix) >= 3:
                return token[: -len(suffix)]
        return token


def verify_claim(
    claim: dict[str, object],
    evidence: Sequence[dict[str, object]],
) -> dict[str, object]:
    return ClaimVerifier().verify(claim, evidence)
