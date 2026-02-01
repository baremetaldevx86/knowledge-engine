from pydantic import BaseModel
import uuid

class SearchResult(BaseModel):
    chunk_id: uuid.UUID
    note_id: uuid.UUID
    note_title: str
    content: str
    score: float
