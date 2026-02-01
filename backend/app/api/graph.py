from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Dict, Any
import random

from app.db import get_session
from app.models import Note, NoteChunk

router = APIRouter()

@router.get("/")
async def get_knowledge_graph(session: AsyncSession = Depends(get_session)):
    """
    Generate graph data (Nodes and Edges).
    Nodes = Notes
    Edges = Semantic similarity between notes
    """
    # 1. Fetch all notes
    result = await session.execute(select(Note))
    notes = result.scalars().all()
    
    nodes = []
    edges = []
    
    if not notes:
        return {"nodes": [], "edges": []}

    # 2. Build Nodes
    for note in notes:
        nodes.append({
            "id": str(note.id),
            "label": note.title,
            "group": "note",
            "val": 10 # Size
        })

    # 3. Build Edges (Simplified)
    # Ideally, for each note, we find its nearest neighbors using vector search.
    # To avoid N queries, we'll do a simplified approach for this prototype:
    # - If we have < 50 notes, we can fetch all chunks and compute pairwise locally? 
    # - OR just run a few queries.
    
    # Practical Approach for Prototype:
    # For every note, query key chunks to find related notes.
    # Optimization: Just link random notes for VISUALIZATION if we don't want to burn compute? 
    # No, let's do real logic: Link notes that share similar chunks.
    
    # Since we can't easily do "all-pairs" efficiently without a dedicated graph DB or loading all vectors,
    # We will pick a few "hub" notes or just iterate the first 10 notes and find their neighbors.
    
    # Real implementation attempt:
    # Iterate top 10 most recent notes, find their top 3 connections.
    
    recent_notes = notes[:10] 
    
    for note in recent_notes:
        # Get one chunk from this note (first one)
        # We need to fetch chunks for this note
        stmt_chunks = select(NoteChunk).where(NoteChunk.note_id == note.id).limit(1)
        chunk_res = await session.execute(stmt_chunks)
        chunk = chunk_res.scalar_one_or_none()
        
        if chunk and chunk.embedding is not None:
            # Search for similar chunks in OTHER notes
            stmt = select(NoteChunk, Note).join(Note) \
                .where(Note.id != note.id) \
                .order_by(NoteChunk.embedding.cosine_distance(chunk.embedding)) \
                .limit(3)
                
            neighbors = await session.execute(stmt)
            for neighbor_chunk, neighbor_note in neighbors:
                # Add edge
                edge_id = f"{note.id}-{neighbor_note.id}"
                # Check duplicates (undirected)
                rev_edge_id = f"{neighbor_note.id}-{note.id}"
                
                # Check if edge already exists in our list (simple check)
                exists = False
                for e in edges:
                    if (e['source'] == str(note.id) and e['target'] == str(neighbor_note.id)) or \
                       (e['source'] == str(neighbor_note.id) and e['target'] == str(note.id)):
                        exists = True
                        break
                
                if not exists:
                    edges.append({
                        "source": str(note.id),
                        "target": str(neighbor_note.id),
                        "value": 1 # Uniform weight for now
                    })

    return {"nodes": nodes, "edges": edges}
