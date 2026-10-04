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
        "n't",
    }
    _predicate_forms = {
        "approve": {"approve", "approved", "approves", "approving"},
        "authorize": {"authorize", "authorized", "authorizes", "authorizing"},
        "confirm": {"confirm", "confirmed", "confirms", "confirming"},
        "endorse": {"endorse", "endorsed", "endorses", "endorsing"},
        "guarantee": {"guarantee", "guaranteed", "guarantees", "guaranteeing"},
        "request": {"request", "requested", "requests", "requesting"},
        "share": {"share", "shared", "shares", "sharing"},
        "register": {"register", "registered", "registers", "registering"},
        "promise": {"promise", "promised", "promises", "promising"},
        "offer": {"offer", "offered", "offers", "offering"},
        "pay": {"pay", "paid", "pays", "paying"},
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
        "cannot",
        "no",
        "not",
        "never",
        "without",
        "does",
        "did",
        "do",
        "has",
        "is",
        "was",
        "were",
        "the",
        "our",
        "your",
        "its",
    }
    _regulators = {"sebi", "rbi", "irdai", "pfrda", "sec", "fca", "cftc"}
    _approval_terms = {"approve", "approved", "authorize", "authorized", "register", "registered"}
    _generic_targets = {
        "scheme", "schemes", "company", "companies", "entity", "entities",
        "platform", "platforms", "investment", "investments", "fund", "funds",
        "product", "products", "service", "services", "offer", "offers",
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
        status = self._determine_status(
            claim_text,
            normalized_evidence,
            claim.get("type"),
        )
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
        claim_type: object = None,
    ) -> str:
        if not evidence:
            return "UNVERIFIED"

        claim_terms = self._meaningful_terms(claim)
        claim_numbers = self._number_terms(claim)
        relevant = []
        supporting = []
        contradicting = []
        regulatory_approval = self._is_regulatory_approval_claim(claim, claim_type)
        target_terms = self._specific_target_terms(claim)

        for item in evidence:
            evidence_text = str(item["text"])
            evidence_terms = self._meaningful_terms(evidence_text)
            overlap = len(claim_terms.intersection(evidence_terms)) / max(len(claim_terms), 1)
            if overlap < 0.25:
                continue
            relevant.append(item)
            if claim_numbers and not claim_numbers.issubset(self._number_terms(evidence_text)):
                continue

            if regulatory_approval and (
                not target_terms or not target_terms.issubset(evidence_terms)
            ):
                continue

            claim_predicates = self._predicates(claim)
            evidence_predicates = self._predicates(evidence_text)
            shared_predicates = claim_predicates.intersection(evidence_predicates)
            if not shared_predicates:
                continue

            claim_negated = self._is_negated_near_predicate(claim, shared_predicates)
            evidence_negated = self._is_negated_near_predicate(evidence_text, shared_predicates)
            if evidence_negated == claim_negated and overlap >= 0.6:
                supporting.append(item)
            elif evidence_negated != claim_negated and overlap >= 0.5:
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

    def _is_negated_near_predicate(self, text: str, predicates: set[str]) -> bool:
        tokens = self._tokens(text)
        for index, token in enumerate(tokens):
            predicate = next(
                (name for name, forms in self._predicate_forms.items() if token in forms),
                None,
            )
            if predicate not in predicates:
                continue
            start = max(0, index - 3)
            end = min(len(tokens), index + 3)
            if any(
                item in self._negation_terms or item.endswith("n't")
                for item in tokens[start:end]
            ):
                return True
        return False

    def _predicates(self, text: str) -> set[str]:
        tokens = set(self._tokens(text))
        return {
            name
            for name, forms in self._predicate_forms.items()
            if tokens.intersection(forms)
        }

    def _is_regulatory_approval_claim(self, claim: str, claim_type: object) -> bool:
        tokens = set(self._tokens(claim))
        return (
            claim_type == "regulatory"
            or bool(tokens.intersection(self._regulators))
            and bool(tokens.intersection(self._approval_terms))
        )

    def _specific_target_terms(self, claim: str) -> set[str]:
        tokens = self._meaningful_terms(claim)
        generic_terms = (
            self._regulators
            | self._approval_terms
            | self._generic_targets
            | {"return", "profit", "high", "fixed", "financial", "guaranteed"}
        )
        generic_terms.update(self._stem(term) for term in tuple(generic_terms))
        return tokens.difference(generic_terms)

    def _meaningful_terms(self, text: str) -> set[str]:
        return {
            self._stem(token)
            for token in self._tokens(text)
            if len(token) >= 3 and token not in self._stop_words
        }

    def _number_terms(self, text: str) -> set[str]:
        return {token for token in self._tokens(text) if any(char.isdigit() for char in token)}

    def _tokens(self, text: str) -> list[str]:
        return [token.lower() for token in re.findall(r"[a-z]+(?:'[a-z]+)?|[0-9]+%?", text.lower())]

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
