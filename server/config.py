import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    memes_dir: Path = Path(os.getenv("MEMES_DIR", ROOT_DIR / "memes"))
    data_dir: Path = Path(os.getenv("DATA_DIR", ROOT_DIR / "data"))
    public_base_url: str = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000").rstrip("/")
    clip_model: str = os.getenv("CLIP_MODEL", "xlm-roberta-base-ViT-B-32")
    clip_pretrained: str = os.getenv("CLIP_PRETRAINED", "laion5b_s13b_b90k")

    @property
    def index_path(self) -> Path:
        return self.data_dir / "vectors.index"

    @property
    def metadata_path(self) -> Path:
        return self.data_dir / "metadata.json"

    @property
    def database_path(self) -> Path:
        return self.data_dir / "gengying.db"


settings = Settings()

