from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
import uuid

from app.db import get_session
from app.models import Note, NoteChunk
from app.schemas import NoteCreate, NoteRead
from app.services.text_processor import TextProcessor
from app.services.embedding import EmbeddingService

router = APIRouter()

import pypdf
import io

@router.post("/upload/", response_model=NoteRead)
async def upload_note(
    file: UploadFile = File(...), 
    session: AsyncSession = Depends(get_session)
):
    content = ""
    
    # 1. Extract Text
    if file.filename.endswith(".pdf"):
        try:
            pdf_bytes = await file.read()
            pdf_file = io.BytesIO(pdf_bytes)
            reader = pypdf.PdfReader(pdf_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid PDF file: {str(e)}")
    else:
        # Assume text/md
        try:
            content_bytes = await file.read()
            content = content_bytes.decode("utf-8")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Could not decode text file.")
            
    if not content.strip():
        raise HTTPException(status_code=400, detail="File is empty or could not extract text.")

    # 2. Process & Save (Reuse logic - ideally refactor this out, but for now duplicate closest logic)
    cleaned_content = TextProcessor.clean(content)
    
    # Use filename as title (remove extension)
    title = file.filename.rsplit(".", 1)[0]
    
    # Save Note
    db_note = Note(title=title, content=cleaned_content)
    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    
    # Chunk & Embed
    chunks = TextProcessor.chunk(cleaned_content)
    
    # Prepare batch inputs
    batch_inputs = [f"Document: {title}\nContent: {chunk}" for chunk in chunks]
    
    # Generate embeddings in batch
    embeddings = await run_in_threadpool(EmbeddingService.generate_batch, batch_inputs)
    
    for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
        db_chunk = NoteChunk(
            note_id=db_note.id,
            chunk_index=idx,
            content=chunk_text,
            embedding=embedding
        )
        session.add(db_chunk)
    
    await session.commit()
    return db_note

@router.post("/", response_model=NoteRead)
async def create_note(note: NoteCreate, session: AsyncSession = Depends(get_session)):
    # 1. Clean text
    cleaned_content = TextProcessor.clean(note.content)
    
    # 2. Save Note
    db_note = Note(title=note.title, content=cleaned_content)
    session.add(db_note)
    await session.commit()
    await session.refresh(db_note)
    
    # 3. Create Chunks
    chunks = TextProcessor.chunk(cleaned_content)
    
    # Prepare batch inputs
    batch_inputs = [f"Document: {note.title}\nContent: {chunk}" for chunk in chunks]
    
    # Generate embeddings in batch
    embeddings = await run_in_threadpool(EmbeddingService.generate_batch, batch_inputs)
    
    for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
        db_chunk = NoteChunk(
            note_id=db_note.id,
            chunk_index=idx,
            content=chunk_text,
            embedding=embedding
        )
        session.add(db_chunk)
    
    await session.commit()
    
    return db_note

@router.get("/", response_model=List[NoteRead])
async def read_notes(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note).offset(skip).limit(limit).order_by(Note.created_at.desc()))
    notes = result.scalars().all()
    return notes

@router.get("/{note_id}", response_model=NoteRead)
async def read_note(note_id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note).where(Note.id == note_id))
    note = result.scalars().first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
