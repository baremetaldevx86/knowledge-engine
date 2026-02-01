import asyncio
from app.db import get_session
from app.models import Note, NoteChunk
from sqlmodel import select

async def check_recent_notes():
    async for session in get_session():
        query = select(Note).order_by(Note.created_at.desc())
        result = await session.execute(query)
        notes = result.scalars().all()
        
        print(f"Found {len(notes)} notes.")
        for i, note in enumerate(notes):
            print(f"ID: {note.id} | Title: {note.title}")
            
            # detailed check for the first (newest) note
            if i == 0:
                 chunk_query = select(NoteChunk).where(NoteChunk.note_id == note.id)
                 chunk_res = await session.execute(chunk_query)
                 chunks = chunk_res.scalars().all()
                 print(f"  -> Chunk Count: {len(chunks)}")
                 if chunks:
                     # Check first 5 chunks to see where ToC is
                     for k in range(min(5, len(chunks))):
                         print(f"  -> Chunk {k} Preview: {chunks[k].content[:200]}...")
                         if "contents" in chunks[k].content.lower():
                             print(f"     [MATCH] 'contents' found in Chunk {k}")

            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(check_recent_notes())
