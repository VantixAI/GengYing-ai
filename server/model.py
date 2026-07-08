from functools import lru_cache
from pathlib import Path
from typing import Iterable

import numpy as np
import open_clip
import torch
from PIL import Image

from .config import settings


class ClipEncoder:
    """A small wrapper around OpenCLIP for normalized text and image embeddings."""

    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            settings.clip_model,
            pretrained=settings.clip_pretrained,
            device=self.device,
        )
        self.tokenizer = open_clip.get_tokenizer(settings.clip_model)
        self.model.eval()

    @staticmethod
    def _normalize(features: torch.Tensor) -> np.ndarray:
        features = features / features.norm(dim=-1, keepdim=True)
        return features.detach().cpu().float().numpy().astype("float32")

    def encode_text(self, texts: list[str]) -> np.ndarray:
        tokens = self.tokenizer(texts).to(self.device)
        with torch.inference_mode():
            features = self.model.encode_text(tokens)
        return self._normalize(features)

    def encode_images(self, paths: Iterable[Path], batch_size: int = 16) -> np.ndarray:
        path_list = list(paths)
        batches: list[np.ndarray] = []
        for start in range(0, len(path_list), batch_size):
            images = []
            for path in path_list[start : start + batch_size]:
                with Image.open(path) as image:
                    images.append(self.preprocess(image.convert("RGB")))
            tensor = torch.stack(images).to(self.device)
            with torch.inference_mode():
                batches.append(self._normalize(self.model.encode_image(tensor)))
        if not batches:
            return np.empty((0, 0), dtype="float32")
        return np.concatenate(batches, axis=0)


@lru_cache(maxsize=1)
def get_encoder() -> ClipEncoder:
    return ClipEncoder()

