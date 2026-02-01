import asyncio
import httpx
import os

async def main():
    if not os.path.exists("test_upload.pdf"):
        print("Please run test_gen_pdf.py first.")
        return

    async with httpx.AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
        files = {'file': ('test_upload.pdf', open("test_upload.pdf", 'rb'), 'application/pdf')}
        
        print("Uploading test_upload.pdf...")
        try:
            response = await client.post("/api/v1/notes/upload/", files=files)
            
            if response.status_code == 200:
                data = response.json()
                print("SUCCESS: Note created via upload.")
                print(f"ID: {data['id']}")
                print(f"Title: {data['title']}")
                print(f"Content Preview: {data['content'][:50]}...")
                
                if "Kronig-Penney" in data['content']:
                    print("VERIFIED: PDF text content was extracted correctly.")
                else:
                    print("FAILURE: Content does not match expected text.")
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
