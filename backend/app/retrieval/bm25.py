import math
import re
from collections import Counter
from collections.abc import Sequence


class BM25Retriever:
    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        if k1 < 0:
            raise ValueError("k1 must be non-negative")
        if not 0 <= b <= 1:
            raise ValueError("b must be between 0 and 1")
        self.k1 = k1
        self.b = b
        self.documents: list[str] = []
        self.tokenized_documents: list[list[str]] = []
        self.term_frequencies: list[Counter[str]] = []
        self.idf: dict[str, float] = {}
        self.average_document_length = 0.0

    @staticmethod
    def tokenize(text: str) -> list[str]:
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return re.findall(r"[a-z0-9]+%?", text.lower())

    def fit(self, documents: Sequence[str | dict[str, object]]) -> "BM25Retriever":
        if not documents:
            raise ValueError("documents must contain at least one item")

        extracted_documents: list[str] = []
        for document in documents:
            if isinstance(document, dict):
                text = document.get("text")
            else:
                text = document
            if not isinstance(text, str) or not text.strip():
                raise ValueError("each document must contain non-empty text")
            extracted_documents.append(text)

        self.documents = extracted_documents
        self.tokenized_documents = [self.tokenize(text) for text in self.documents]
        self.term_frequencies = [Counter(tokens) for tokens in self.tokenized_documents]
        self.average_document_length = sum(
            len(tokens) for tokens in self.tokenized_documents
        ) / len(self.tokenized_documents)

        document_frequency: Counter[str] = Counter()
        for tokens in self.tokenized_documents:
            document_frequency.update(set(tokens))

        document_count = len(self.documents)
        self.idf = {
            term: math.log(
                1 + (document_count - frequency + 0.5) / (frequency + 0.5)
            )
            for term, frequency in document_frequency.items()
        }
        return self

    def score(self, query: str, document_index: int) -> float:
        if not self.documents:
            raise RuntimeError("fit must be called before scoring")
        if not 0 <= document_index < len(self.documents):
            raise IndexError("document_index is out of range")

        query_terms = Counter(self.tokenize(query))
        document_terms = self.term_frequencies[document_index]
        document_length = len(self.tokenized_documents[document_index])
        score = 0.0

        for term, query_frequency in query_terms.items():
            if term not in document_terms:
                continue
            term_frequency = document_terms[term]
            numerator = term_frequency * (self.k1 + 1)
            denominator = term_frequency + self.k1 * (
                1 - self.b + self.b * document_length / self.average_document_length
            )
            score += self.idf[term] * (numerator / denominator) * query_frequency
        return score

    def search(self, query: str, top_k: int = 5) -> list[dict[str, object]]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        if not self.documents:
            raise RuntimeError("fit must be called before searching")

        ranked = sorted(
            (
                {
                    "text": document,
                    "score": self.score(query, index),
                }
                for index, document in enumerate(self.documents)
            ),
            key=lambda result: result["score"],
            reverse=True,
        )
        return [
            {**result, "rank": rank}
            for rank, result in enumerate(ranked[:top_k], start=1)
        ]
