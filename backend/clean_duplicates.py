import asyncio
from app.db import get_session
from app.models import Note, NoteChunk
from sqlmodel import select, delete

async def deduplicate_notes():
    async for session in get_session():
        # Get all notes ordered by creation time
        result = await session.execute(select(Note).order_by(Note.created_at.desc()))
        notes = result.scalars().all()
        
        seen_titles = set()
        notes_to_keep = []
        notes_to_delete = []
        
        for note in notes:
            if note.title not in seen_titles:
                seen_titles.add(note.title)
                notes_to_keep.append(note)
            else:
                notes_to_delete.append(note)
                
        print(f"Total Notes: {len(notes)}")
        print(f"Unique Titles: {len(seen_titles)}")
        print(f"Deleting {len(notes_to_delete)} duplicates...")
        
        for note in notes_to_delete:
            print(f" - Deleting {note.title} (ID: {note.id})")
            # Delete chunks first
            await session.execute(delete(NoteChunk).where(NoteChunk.note_id == note.id))
            # Delete note
            await session.execute(delete(Note).where(Note.id == note.id))
            
        await session.commit()
        print("Deduplication complete.")

if __name__ == "__main__":
    asyncio.run(deduplicate_notes())
