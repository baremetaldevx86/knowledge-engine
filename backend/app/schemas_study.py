from pydantic import BaseModel
from typing import List

class Flashcard(BaseModel):
    front: str
    back: str

class FlashcardSet(BaseModel):
    note_id: str
    cards: List[Flashcard]

class GenerateFlashcardsRequest(BaseModel):
    note_id: str
    amount: int = 5
