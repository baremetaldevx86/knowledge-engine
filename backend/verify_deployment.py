import requests
import sys
import time

def verify_backend(base_url):
    print(f"🔍 Verifying Backend at: {base_url}")
    print("-" * 50)
    
    # Ensure no trailing slash
    base_url = base_url.rstrip("/")
    
    # 1. Health Check (Root)
    try:
        print("[1/4] Checking Root Endpoint (Health)... ", end="")
        resp = requests.get(f"{base_url}/")
        if resp.status_code == 200:
            print("✅ OK")
        else:
            print(f"❌ FAILED ({resp.status_code})")
            print(f"      Response: {resp.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return

    # 2. Database Check (List Notes)
    try:
        print("[2/4] Checking Database Connection (GET /notes)... ", end="")
        resp = requests.get(f"{base_url}/api/v1/notes/")
        if resp.status_code == 200:
            notes = resp.json()
            print(f"✅ OK (Found {len(notes)} notes)")
        else:
            print(f"❌ FAILED ({resp.status_code})")
            print(f"      Response: {resp.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    # 3. Vector Search Check
    try:
        print("[3/4] Checking Vector DB (Search 'test')... ", end="")
        resp = requests.get(f"{base_url}/api/v1/search/?q=test&limit=1")
        if resp.status_code == 200:
            print("✅ OK")
        else:
            print(f"❌ FAILED ({resp.status_code})")
            # 500 often means pgvector is missing
            if "vector" in resp.text.lower():
                print("      👉 HINT: Did you authorize 'CREATE EXTENSION vector' in your database?")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    # 4. Graph API Check
    try:
        print("[4/4] Checking Knowledge Graph... ", end="")
        resp = requests.get(f"{base_url}/api/v1/graph/")
        if resp.status_code == 200:
            print("✅ OK")
        else:
            print(f"❌ FAILED ({resp.status_code})")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    print("-" * 50)
    print("If all checks passed, your Backend & Database are healthy! 🚀")

if __name__ == "__main__":
    print("Knowledge Engine Deployment Verifier")
    print("Usage: python verify_deployment.py <YOUR_BACKEND_URL>")
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter your Backend URL (e.g., https://myapp.onrender.com): ")
    
    if url:
        verify_backend(url)
    else:
        print("No URL provided.")
