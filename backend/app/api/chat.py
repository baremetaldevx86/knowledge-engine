from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.concurrency import run_in_threadpool
from sqlmodel import select

from app.db import get_session
from app.models import Note, NoteChunk
from app.schemas_chat import ChatRequest, ChatResponse
from app.services.embedding import EmbeddingService
from app.services.llm import LLMService

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_notes(
    request: ChatRequest,
    session: AsyncSession = Depends(get_session)
):
    try:
        # 1. Retrieve relevant chunks
        query_embedding = await run_in_threadpool(EmbeddingService.generate, request.query)
        
        # Determine strictness/limit. Top 5 chunks is usually good.
        # Determine strictness/limit. Top 5 chunks is usually good.
        stmt = select(NoteChunk, Note)\
            .join(Note)\
            .order_by(NoteChunk.embedding.cosine_distance(query_embedding))\
            .limit(5)
            
        result = await session.execute(stmt)
        chunks_with_notes = result.all() # returns list of (NoteChunk, Note) tuples
        
        chunks = [c[0] for c in chunks_with_notes]
        
        if not chunks:
            # Fallback: If no chunks found, try to just fetch the latest note to helpful?
            # Or just proceed.
            pass

        # 2. Construct Context
        context_parts = []
        
        # A. Always inject the most recent note as "Active Context" (Critical for "what is the doc about" queries)
        recent_note_stmt = select(Note).order_by(Note.created_at.desc()).limit(1)
        recent_note_res = await session.execute(recent_note_stmt)
        recent_note = recent_note_res.scalars().first()
        
        # A. Always inject the most recent note as "Active Context" (Critical for "what is the doc about" queries)
        recent_note_stmt = select(Note).order_by(Note.created_at.desc()).limit(1)
        recent_note_res = await session.execute(recent_note_stmt)
        recent_note = recent_note_res.scalars().first()
        
        if recent_note:
            # Fetch first 3 chunks to capture Intro + Table of Contents
            recent_chunks_stmt = select(NoteChunk).where(NoteChunk.note_id == recent_note.id).order_by(NoteChunk.chunk_index).limit(3)
            recent_chunks_res = await session.execute(recent_chunks_stmt)
            start_chunks = recent_chunks_res.scalars().all()
            
            full_snippet = "\n".join([c.content for c in start_chunks])
            context_parts.append(f"SOURCE [MOST_RECENT_UPLOAD START]: {recent_note.title}\nCONTENT_SNIPPET: {full_snippet}\n...\n(This is the beginning of the user's latest file. Use this for ToC/Summary questions.)\n")

        # B. Add Retrieval Results
        for chunk, note in chunks_with_notes:
            # Avoid duplicating if it's the same note/content, but for now simple append is robust
            context_parts.append(f"SOURCE [SEARCH_RESULT]: {note.title}\nCONTENT: {chunk.content}")
            
        context_text = "\n\n---\n\n".join(context_parts)
        
        # 3. Call LLM
        answer = await LLMService.generate_answer(request.query, context_text)
        
        # 4. Return response with sources (note IDs or titles)
        return ChatResponse(answer=answer, sources=[str(c.note_id) for c in chunks])
        
    except ValueError as e:
         raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
