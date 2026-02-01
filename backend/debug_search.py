import asyncio
from app.db import get_session
from app.models import NoteChunk
from app.services.embedding import EmbeddingService
from sqlmodel import select
from fastapi.concurrency import run_in_threadpool

async def debug_search():
    query_text = "List the table of contents"
    print(f"Query: {query_text}")
    
    # 1. Generate embedding
    print("Generating embedding...")
    query_embedding = EmbeddingService.generate(query_text)
    print(f"Embedding generated. Shape: {len(query_embedding)}")
    
    # 2. Search
    print("Executing search...")
    async for session in get_session():
        try:
            stmt = select(NoteChunk).order_by(NoteChunk.embedding.cosine_distance(query_embedding)).limit(5)
            result = await session.execute(stmt)
            chunks = result.scalars().all()
            
            print(f"Chunks found: {len(chunks)}")
            for chunk in chunks:
                print(f"Chunk ID: {chunk.id}, Score: ?")
                print(f"Content: {chunk.content[:100]}...")
        except Exception as e:
            print(f"Search failed: {e}")

if __name__ == "__main__":
    asyncio.run(debug_search())
