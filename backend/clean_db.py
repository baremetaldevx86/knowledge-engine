import asyncio
from app.db import get_session
from app.models import Note, NoteChunk
from sqlmodel import select, delete

async def clean_db():
    titles_to_delete = [
        "Cats", 
        "Test Note", 
        "test_upload", 
        "Chunk Test", 
        "Space", 
        "Photosynthesis"
    ]
    
    async for session in get_session():
        print("Starting cleanup...")
        
        # 1. Delete Chunks first (foreign key constraint usually handles this if cascade is set, but let's be safe/explicit if needed, 
        # actually SQLModel/Postgres usually needs explicit cascade or manual delete if not configured)
        # Let's check IDs first
        
        stmt = select(Note).where(Note.title.in_(titles_to_delete))
        result = await session.execute(stmt)
        notes_to_delete = result.scalars().all()
        
        if not notes_to_delete:
            print("No junk notes found.")
            return

        print(f"Found {len(notes_to_delete)} notes to delete.")
        
        for note in notes_to_delete:
            print(f"Deleting note: {note.title} (ID: {note.id})")
            
            # Delete chunks for this note
            delete_chunks = delete(NoteChunk).where(NoteChunk.note_id == note.id)
            await session.execute(delete_chunks)
            
            # Delete note
            delete_note = delete(Note).where(Note.id == note.id)
            await session.execute(delete_note)
            
        await session.commit()
        print("Cleanup complete.")

if __name__ == "__main__":
    asyncio.run(clean_db())
