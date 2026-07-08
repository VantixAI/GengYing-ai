from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import initialize_database, record_click, register_meme
from .schemas import ClickRequest, SearchRequest, SearchResponse, UploadResponse
from .search import search_engine


ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings.memes_dir.mkdir(parents=True, exist_ok=True)
    initialize_database()
    yield


app = FastAPI(
    title="GengYing AI API",
    description="Semantic meme search powered by CLIP and FAISS.",
    version="0.1.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
settings.memes_dir.mkdir(parents=True, exist_ok=True)
app.mount("/memes", StaticFiles(directory=settings.memes_dir), name="memes")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/search", response_model=SearchResponse)
def search_memes(payload: SearchRequest) -> SearchResponse:
    try:
        results = search_engine.search(payload.query, payload.limit)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return SearchResponse(query=payload.query, results=results)


@app.post("/api/clicks", status_code=204)
def create_click(payload: ClickRequest) -> None:
    record_click(payload.meme_id, payload.query)


@app.post("/api/memes/upload", response_model=UploadResponse)
async def upload_meme(file: UploadFile = File(...)) -> UploadResponse:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="仅支持 JPG、PNG、WEBP 和 GIF 图片")
    contents = await file.read(MAX_UPLOAD_SIZE + 1)
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="图片不能超过 10 MB")

    suffix = ALLOWED_TYPES[file.content_type]
    stem = Path(file.filename or "meme").stem[:50]
    filename = f"{stem}-{uuid4().hex[:8]}{suffix}"
    (settings.memes_dir / filename).write_bytes(contents)
    meme_id = register_meme(filename)
    return UploadResponse(id=meme_id, filename=filename, message="上传成功，请重新建立索引")

