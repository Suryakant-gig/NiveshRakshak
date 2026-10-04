"""Embedding model and vector retrieval helpers."""

from collections.abc import Sequence

from sentence_transformers import SentenceTransformer


class SentenceTransformerEmbedder:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        normalize_embeddings: bool = True,
    ) -> None:
        self.model = SentenceTransformer(model_name)
        self.normalize_embeddings = normalize_embeddings

    def encode(self, texts: str | Sequence[str]) -> list[dict[str, str | list[float]]]:
        if isinstance(texts, str):
            values = [texts]
        else:
            values = list(texts)

        if not values or any(not isinstance(text, str) or not text.strip() for text in values):
            raise ValueError("texts must contain at least one non-empty string")

        vectors = self.model.encode(
            values,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize_embeddings,
        )
        return [
            {
                "text": text,
                "embedding": vector.tolist() if hasattr(vector, "tolist") else list(vector),
            }
            for text, vector in zip(values, vectors)
        ]

    def encode_query(self, text: str) -> dict[str, str | list[float]]:
        return self.encode(text)[0]

    def encode_documents(self, texts: Sequence[str]) -> list[dict[str, str | list[float]]]:
        return self.encode(texts)
