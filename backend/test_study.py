import asyncio
import httpx
import sys

async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=60.0) as client:
        # 1. Create a note to study
        print("Creating test note...")
        note_content = "Photosynthesis is the process used by plants, algae and certain bacteria to harness energy from sunlight and turn it into chemical energy. The process is performed by plants, algae, and some types of bacteria, which capture energy from sunlight to produce oxygen (O2) and chemical energy stored in glucose (a sugar). Herbivores then obtain this energy by eating plants, and carnivores obtain it by eating herbivores. The process involves chlorophyll which gives plants their green color."
        
        create_res = await client.post("/api/v1/notes/", json={"title": "Photosynthesis", "content": note_content})
        
        if create_res.status_code != 200:
            print(f"Failed to create note: {create_res.text}")
            return
            
        note_id = create_res.json()["id"]
        print(f"Note created: {note_id}")
        
        # 2. Generate Flashcards
        print("Generating flashcards...")
        res = await client.post("/api/v1/study/flashcards", json={"note_id": note_id, "amount": 3})
        
        if res.status_code != 200:
            print(f"Error: {res.text}")
            return
            
        data = res.json()
        print(f"Flashcards generated for note: {data['note_id']}")
        for i, card in enumerate(data['cards']):
            print(f"  Card {i+1}: Q: {card['front']} | A: {card['back']}")
            
        if len(data['cards']) > 0:
            print("SUCCESS: Flashcards generated.")

if __name__ == "__main__":
    asyncio.run(main())
