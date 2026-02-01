from typing import List, Optional
from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field, Relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

class NoteChunk(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    note_id: uuid.UUID = Field(foreign_key="note.id")
    chunk_index: int
    content: str
    embedding: Optional[List[float]] = Field(default=None, sa_column=Column(Vector(384))) # 384 for all-MiniLM-L6-v2

    note: Optional["Note"] = Relationship(back_populates="chunks")

class Note(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    content: str # Original full content
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    chunks: List[NoteChunk] = Relationship(back_populates="note")
