import os
import httpx
import asyncio
from dotenv import load_dotenv

# Force load .env
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
print(f"Loading .env from: {env_path}")
load_dotenv(env_path)

KEY = os.getenv("OPENROUTER_API_KEY")
print(f"Key loaded: {bool(KEY)}")
if KEY:
    print(f"Key prefix: {KEY[:5]}...")

async def test_key():
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json"
    }
    
    print(f"Testing key against {url}...")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            print(f"Status Code: {resp.status_code}")
            if resp.status_code == 200:
                print("SUCCESS: Key is valid!")
            else:
                print(f"FAILURE: API returned {resp.status_code}")
                print(f"Response: {resp.text}")
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")

if __name__ == "__main__":
    if not KEY:
        print("ERROR: No key found in environment.")
    else:
        asyncio.run(test_key())
