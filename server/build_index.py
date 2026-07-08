import json
from pathlib import Path

import faiss

from .config import settings
from .database import initialize_database, register_meme
from .model import get_encoder


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def find_images() -> list[Path]:
    return sorted(
        path
        for path in settings.memes_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def build_index() -> None:
    settings.memes_dir.mkdir(parents=True, exist_ok=True)
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    initialize_database()
    images = find_images()
    if not images:
        raise SystemExit(f"没有找到图片，请先把表情包放入 {settings.memes_dir}")

    print(f"正在为 {len(images)} 张图片提取 CLIP 向量……")
    vectors = get_encoder().encode_images(images)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    metadata = [
        {"id": register_meme(path.name), "filename": path.name}
        for path in images
    ]

    faiss.write_index(index, str(settings.index_path))
    settings.metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"索引已保存到 {settings.index_path}")


if __name__ == "__main__":
    build_index()

