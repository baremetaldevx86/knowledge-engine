from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import json
import uuid

from app.db import get_session
from app.models import Note
from app.schemas_study import Flashcard, FlashcardSet, GenerateFlashcardsRequest
from app.services.llm import LLMService

router = APIRouter()

@router.post("/flashcards", response_model=FlashcardSet)
async def generate_flashcards(
    request: GenerateFlashcardsRequest,
    session: AsyncSession = Depends(get_session)
):
    # 1. Fetch Note
    stmt = select(Note).where(Note.id == uuid.UUID(request.note_id))
    result = await session.execute(stmt)
    note = result.scalar_one_or_none()
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
        
    # 2. Prompt LLM
    prompt = f"""
    Create {request.amount} flashcards for studying the following note.
    Return ONLY a raw JSON array of objects with "front" and "back" keys. 
    Do not include markdown formatting (like ```json), just the raw JSON string.
    
    Note Content:
    {note.content[:3000]} 
    """
    
    # We use a dummy query context for the answer generation method or repurpose it?
    # Our LLMService is designed for RAG (QA). We should ideally add a generic `complete` method.
    # But `generate_answer` takes (query, context). We can abuse it:
    # Query = Prompt
    # Context = "" (since we embedded content in prompt)
    
    response_text = await LLMService.generate_answer(prompt, "")
    
    # 3. Parse JSON
    try:
        # cleanup markdown if present
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        cards_data = json.loads(clean_json)
        
        cards = [Flashcard(**c) for c in cards_data]
        return FlashcardSet(note_id=request.note_id, cards=cards)
        
    except Exception as e:
        print(f"Failed to generate flashcards: {e}")
        # Fallback if parsing fails or LLM is dumb
        return FlashcardSet(note_id=request.note_id, cards=[
            Flashcard(front="Error", back="Could not generate flashcards. Try again.")
        ])
