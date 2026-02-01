import asyncio
from app.db import get_session
from app.models import Note, NoteChunk
from sqlmodel import select, delete

async def delete_bad_node():
    target_id = "35003f06-3bd4-40ec-bc4a-e20fe3059456" # From debug output
    
    async for session in get_session():
        print(f"Deleting note {target_id}...")
        
        # Delete chunks
        delete_chunks = delete(NoteChunk).where(NoteChunk.note_id == target_id)
        await session.execute(delete_chunks)
        
        # Delete note
        delete_note = delete(Note).where(Note.id == target_id)
        await session.execute(delete_note)
            
        await session.commit()
        print("Done.")

if __name__ == "__main__":
    asyncio.run(delete_bad_node())
