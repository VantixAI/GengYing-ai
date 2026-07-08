from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=300)
    limit: int = Field(default=6, ge=1, le=20)


class MemeResult(BaseModel):
    id: int
    filename: str
    url: str
    score: float
    captions: list[str]


class SearchResponse(BaseModel):
    query: str
    results: list[MemeResult]


class ClickRequest(BaseModel):
    meme_id: int
    query: str = Field(min_length=1, max_length=300)


class UploadResponse(BaseModel):
    id: int
    filename: str
    message: str

