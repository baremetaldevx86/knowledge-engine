import asyncio
import httpx

async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=60.0) as client:
        # We assume "Cats" and "Space" notes exist from previous test.
        
        # 3. Ask a question about Cats
        print("Asking: 'What are cats?'")
        response = await client.post("/api/v1/chat/", json={"query": "What are cats?"})
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return
            
        data = response.json()
        print(f"Answer: {data['answer']}")
        print(f"Sources: {data['sources']}")
        
        if "mammal" in data['answer'].lower() or "pet" in data['answer'].lower():
            print("SUCCESS: Answer seems relevant.")
        else:
            print("WARNING: Answer might not be relevant. Check context.")

if __name__ == "__main__":
    asyncio.run(main())
