import asyncio
import httpx

async def main():
    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
        print("Fetching Knowledge Graph...")
        response = await client.get("/api/v1/graph/")
        
        if response.status_code != 200:
            print(f"Error: {response.text}")
            return
            
        data = response.json()
        print(f"Nodes: {len(data['nodes'])}")
        print(f"Edges: {len(data['edges'])}")
        
        if len(data['nodes']) > 0:
            print("SUCCESS: Graph data returned.")
        else:
            print("WARNING: No nodes found (make sure notes exist).")

if __name__ == "__main__":
    asyncio.run(main())
