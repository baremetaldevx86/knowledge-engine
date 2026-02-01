import asyncio
import httpx

async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
        # 1. Create a note about Cats
        print("Creating note about Cats...")
        await client.post("/api/v1/notes/", json={
            "title": "Cats", 
            "content": "Cats are small carnivorous mammals. They are often kept as house pets."
        })
        
        # 2. Create a note about Space
        print("Creating note about Space...")
        await client.post("/api/v1/notes/", json={
            "title": "Space", 
            "content": "The universe is vast and contains many galaxies, stars, and planets."
        })
        
        # 3. Search for "kitten" (should match Cats, not Space)
        print("\nSearching for 'kitten'...")
        response = await client.get("/api/v1/search/", params={"q": "kitten", "limit": 1})
        results = response.json()
        
        for res in results:
            print(f"Match: {res['note_title']} - Score (Distance): {res['score']}")
            
        if results and results[0]['note_title'] == "Cats":
            print("SUCCESS: 'kitten' matched 'Cats'")
        else:
            print("FAILURE: Semantic search did not return expected result.")

if __name__ == "__main__":
    asyncio.run(main())
