import asyncio
from app.db import init_db, get_session
from app.models import Note
from sqlmodel import select

async def main():
    print("Initializing DB...")
    await init_db()
    print("DB Initialized.")
    
    print("Creating a test note...")
    async for session in get_session():
        note = Note(title="Test Note", content="This is a test note to verify DB connection.")
        session.add(note)
        await session.commit()
        await session.refresh(note)
        print(f"Note created with ID: {note.id}")
        
        # Verify fetch
        result = await session.execute(select(Note).where(Note.id == note.id))
        fetched_note = result.scalars().first()
        print(f"Fetched note: {fetched_note.title}")

if __name__ == "__main__":
    asyncio.run(main())
