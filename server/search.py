import json
from dataclasses import dataclass
from urllib.parse import quote

import faiss

from .captions import generate_captions
from .config import settings
from .model import get_encoder


@dataclass
class SearchResult:
    id: int
    filename: str
    url: str
    score: float
    captions: list[str]


class MemeSearchEngine:
    def __init__(self) -> None:
        self.index: faiss.Index | None = None
        self.metadata: list[dict] = []
        self.reload()

    def reload(self) -> None:
        if not settings.index_path.exists() or not settings.metadata_path.exists():
            self.index = None
            self.metadata = []
            return
        self.index = faiss.read_index(str(settings.index_path))
        self.metadata = json.loads(settings.metadata_path.read_text(encoding="utf-8"))

    def search(self, query: str, limit: int = 6) -> list[SearchResult]:
        if self.index is None or not self.metadata:
            raise RuntimeError("表情包索引尚未建立，请先运行 python -m server.build_index")

        vector = get_encoder().encode_text([query])
        count = min(limit, len(self.metadata))
        scores, positions = self.index.search(vector, count)
        captions = generate_captions(query)

        results = []
        for score, position in zip(scores[0], positions[0]):
            if position < 0:
                continue
            item = self.metadata[int(position)]
            filename = item["filename"]
            results.append(
                SearchResult(
                    id=int(item["id"]),
                    filename=filename,
                    url=f"{settings.public_base_url}/memes/{quote(filename)}",
                    score=max(0.0, min(1.0, float(score))),
                    captions=captions,
                )
            )
        return results


search_engine = MemeSearchEngine()

