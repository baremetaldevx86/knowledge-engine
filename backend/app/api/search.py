from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, col
from typing import List

from app.db import get_session
from app.models import Note, NoteChunk
from app.schemas_search import SearchResult
from app.services.embedding import EmbeddingService

router = APIRouter()

@router.get("/", response_model=List[SearchResult])
async def search_notes(
    q: str = Query(..., description="Query text"),
    limit: int = 5,
    session: AsyncSession = Depends(get_session)
):
    # 1. Generate embedding for query
    query_embedding = await run_in_threadpool(EmbeddingService.generate, q)
    
    # 2. Search using pgvector cosine distance (L2 distance is <->, cosine is <=>) 
    # Use cosine_distance for now. Note: pgvector cosine operator is <=>
    # Lower distance = more similar. 
    # To get similarity score (0-1), we can do 1 - distance.
    
    # Correct sqlalchemy syntax for pgvector with sqlmodel
    stmt = select(NoteChunk, Note).join(Note) \
        .order_by(NoteChunk.embedding.cosine_distance(query_embedding)) \
        .limit(limit)
        
    result = await session.execute(stmt)
    rows = result.all()
    
    results = []
    for chunk, note in rows:
        # Calculate score (optional, can retrieve distance also)
        # We can re-calculate distance or just return rows.
        # For simplicity, let's just return the sorted results.
        
        results.append(SearchResult(
            chunk_id=chunk.id,
            note_id=note.id,
            note_title=note.title,
            content=chunk.content,
            score=0.0 # Placeholder, getting actual distance requires modifying select
        ))
        
    return results
