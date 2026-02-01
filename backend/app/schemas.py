from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: uuid.UUID
    created_at: datetime
