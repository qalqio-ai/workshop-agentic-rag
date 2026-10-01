import hashlib
import re
from dataclasses import dataclass

from qdrant_client import QdrantClient, models

from .config import settings


@dataclass
class Evidence:
    source_id: str
    title: str
    chunk_id: str
    text: str
    score: float


class HashEmbedder:
    """Stable offline embedding for tests and the zero-credential demo mode."""

    def embed(self, text: str) -> list[float]:
        vec = [0.0] * settings.vector_size
        stopwords = {"a", "an", "and", "do", "for", "how", "i", "is", "it", "of", "the", "to", "what", "with"}
        for token in re.findall(r"[a-z0-9]+", text.lower()):
            if token in stopwords:
                continue
            digest = hashlib.blake2b(token.encode(), digest_size=4).digest()
            idx = int.from_bytes(digest, "big") % settings.vector_size
            vec[idx] += 1.0
        norm = sum(value * value for value in vec) ** 0.5 or 1.0
        return [value / norm for value in vec]


class FastEmbedder:
    def __init__(self):
        from fastembed import TextEmbedding

        self.model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def embed(self, text: str) -> list[float]:
        return next(self.model.embed([text])).tolist()


class ProfileStore:
    def __init__(self, path: str, in_memory: bool = False):
        self.client = QdrantClient(location=":memory:") if in_memory else QdrantClient(path=path)
        self.embedder = HashEmbedder() if settings.model_provider == "mock" or in_memory else FastEmbedder()

    def _collection(self, use_case_id: str) -> str:
        return "profile_" + use_case_id.replace("-", "_")

    def is_available(self) -> bool:
        try:
            self.client.get_collections()
        except Exception:
            return False
        return True

    def add(self, use_case_id: str, source_id: str, title: str, text: str) -> str:
        collection = self._collection(use_case_id)
        if not self.client.collection_exists(collection):
            self.client.create_collection(
                collection_name=collection,
                vectors_config=models.VectorParams(size=settings.vector_size, distance=models.Distance.COSINE),
            )
        chunks = _chunks(text)
        points = []
        for index, chunk in enumerate(chunks):
            chunk_id = f"{source_id}-{index + 1:03d}"
            payload = {"source_id": source_id, "title": title, "chunk_id": chunk_id, "text": chunk}
            points.append(
                models.PointStruct(
                    id=_point_id(use_case_id, chunk_id),
                    vector=self.embedder.embed(chunk),
                    payload=payload,
                )
            )
        self.client.upsert(collection_name=collection, points=points, wait=True)
        return str(points[0].payload["chunk_id"])

    def search(self, use_case_id: str, query: str, limit: int = 5) -> list[Evidence]:
        collection = self._collection(use_case_id)
        if not self.client.collection_exists(collection):
            return []
        result = self.client.query_points(
            collection_name=collection,
            query=self.embedder.embed(query),
            limit=limit,
            with_payload=True,
        ).points
        return [
            Evidence(
                source_id=str(point.payload["source_id"]),
                title=str(point.payload["title"]),
                chunk_id=str(point.payload["chunk_id"]),
                text=str(point.payload["text"]),
                score=float(point.score or 0),
            )
            for point in result
        ]

    def close(self) -> None:
        self.client.close()


def _point_id(profile_id: str, chunk_id: str) -> int:
    digest = hashlib.sha256(f"{profile_id}:{chunk_id}".encode()).digest()[:8]
    return int.from_bytes(digest, "big") & 0x7FFF_FFFF_FFFF_FFFF


def _chunks(text: str, max_chars: int = 900) -> list[str]:
    paragraphs = [part.strip() for part in text.splitlines() if part.strip()]
    chunks, current = [], ""
    for paragraph in paragraphs or [text.strip()]:
        if current and len(current) + len(paragraph) + 1 > max_chars:
            chunks.append(current)
            current = ""
        current = (current + "\n" + paragraph).strip()
    if current:
        chunks.append(current)
    return chunks
