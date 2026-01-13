import asyncio
import os
import httpx
from dotenv import load_dotenv

# Load .env
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "backend", ".env")
load_dotenv(env_path, override=True)

API_KEY = os.getenv("OPENROUTER_API_KEY")

async def test_openrouter():
    print(f"Testing with API Key: {API_KEY[:6]}... (Length: {len(API_KEY) if API_KEY else 0})")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "Vibe Coder Debug",
    }
    
    # Test with the problematic model first
    models = [
        "google/gemma-3n-e2b-it:free",
        "tngtech/deepseek-r1t2-chimera:free",
        "meta-llama/llama-3-8b-instruct:free" # Alternative to try
    ]
    
    for model in models:
        print(f"\n--- Testing Model: {model} ---")
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, say hi!"}
            ]
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                print(f"Status Code: {response.status_code}")
                print(f"Response Body: {response.text}")
                
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_openrouter())
