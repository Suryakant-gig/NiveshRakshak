"""Retrieval tests."""
import math

import pytest

from backend.app.evidence.search import ClaimSourceSearch
from backend.app.evidence.verifier import ClaimVerifier
from backend.app.retrieval import embeddings, reranker
from backend.app.retrieval.bm25 import BM25Retriever
from backend.app.retrieval.hybrid import RRFFusion
from backend.app.retrieval.reranker import CrossEncoderReranker


class FakeVectors(list):
    def tolist(self):
        return list(self)


class FakeSentenceTransformer:
    def __init__(self, model_name):
        self.model_name = model_name

    def encode(self, values, **kwargs):
        vectors = []
        for value in values:
            lowered = value.lower()
            vectors.append([
                float("return" in lowered or "profit" in lowered),
                float("phishing" in lowered or "otp" in lowered),
                float("weather" in lowered or "rain" in lowered),
            ])
        return FakeVectors(vectors)


class FakeCrossEncoder:
    def __init__(self, model_name, max_length):
        self.model_name = model_name
        self.max_length = max_length

    def predict(self, pairs):
        return [2.0 if "return" in evidence.lower() else -1.0 for _, evidence in pairs]


def test_embeddings_return_structured_vectors(monkeypatch):
    monkeypatch.setattr(embeddings, "SentenceTransformer", FakeSentenceTransformer)
    model = embeddings.SentenceTransformerEmbedder()

    result = model.encode_query("Guaranteed return")

    assert result["text"] == "Guaranteed return"
    assert result["embedding"] == [1.0, 0.0, 0.0]


def test_embeddings_reject_empty_text(monkeypatch):
    monkeypatch.setattr(embeddings, "SentenceTransformer", FakeSentenceTransformer)
    model = embeddings.SentenceTransformerEmbedder()

    with pytest.raises(ValueError):
        model.encode_documents([""])


def test_bm25_ranks_matching_terms_and_filters_zero_scores():
    retriever = BM25Retriever().fit([
        "Guaranteed investment return",
        "Rain is expected tomorrow",
    ])

    results = retriever.search("guaranteed return", top_k=5)

    assert len(results) == 1
    assert results[0]["text"] == "Guaranteed investment return"
    assert results[0]["rank"] == 1


def test_bm25_preserves_english_financial_tokens():
    tokens = BM25Retriever.tokenize("Guaranteed 30% return")

    assert tokens == ["guaranteed", "30%", "return"]


def test_rrf_rewards_documents_present_in_both_rankings():
    fusion = RRFFusion()
    results = fusion.fuse(
        [{"text": "A"}, {"text": "B"}],
        [{"text": "B"}, {"text": "A"}],
        top_k=2,
    )

    assert all(result["sources"] == ["bm25", "vector"] for result in results)
    assert all(result["rrf_score"] == pytest.approx(1 / 61 + 1 / 62) for result in results)


def test_cross_encoder_preserves_raw_score_and_normalizes_relevance(monkeypatch):
    monkeypatch.setattr(reranker, "CrossEncoder", FakeCrossEncoder)
    model = CrossEncoderReranker()

    results = model.rerank(
        "Guaranteed return",
        [
            {"source": "source_a", "text": "A guaranteed return warning"},
            {"source": "source_b", "text": "Weather forecast"},
        ],
    )

    assert results[0]["source"] == "source_a"
    assert results[0]["reranker_score"] == 2.0
    assert 0 < results[0]["relevance_score"] < 1
    assert math.isclose(results[0]["relevance_score"], 1 / (1 + math.exp(-2)))


def test_source_search_extracts_url_and_classifies_official_source():
    result = ClaimSourceSearch().search(
        {"id": "claim_001", "text": "Guaranteed return warning"},
        [{
            "text": "Read https://sebi.gov.in/notice for the guaranteed return warning.",
            "score": 0.9,
        }],
    )

    evidence = result["evidence"][0]
    assert evidence["source"] == "sebi.gov.in"
    assert evidence["source_type"] == "official_regulator"
    assert evidence["channel"] == "web"


def test_verifier_supports_matching_negation():
    result = ClaimVerifier().verify(
        {"id": "claim_001", "text": "Banks do not request OTPs"},
        [{
            "source": "RBI",
            "text": "Banks do not request OTPs from customers.",
            "relevance_score": 0.93,
        }],
    )

    assert result["status"] == "SUPPORTED"
    assert set(result) == {"claim_id", "status", "evidence"}


def test_verifier_contradicts_explicit_negation():
    result = ClaimVerifier().verify(
        {"id": "claim_002", "text": "Banks request OTPs from customers"},
        [{
            "source": "RBI",
            "text": "Banks do not request OTPs from customers.",
            "relevance_score": 0.93,
        }],
    )

    assert result["status"] == "CONTRADICTED"


def test_verifier_returns_unverified_without_evidence():
    result = ClaimVerifier().verify(
        {"id": "claim_003", "text": "A claim with no available source"},
        [],
    )

    assert result == {
        "claim_id": "claim_003",
        "status": "UNVERIFIED",
        "evidence": [],
    }
