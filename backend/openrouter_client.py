import httpx
import os
from dotenv import load_dotenv

# Load .env from possible locations and validate API key
# First, try loading .env located in the same directory as this file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, ".env")
load_dotenv(env_path, override=True)
# Fallback: try loading .env from the project root (one level up)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
fallback_path = os.path.join(project_root, ".env")
if not os.getenv("OPENROUTER_API_KEY"):
    load_dotenv(fallback_path, override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print(f"DEBUG: Loaded .env from {env_path if os.getenv('OPENROUTER_API_KEY') else fallback_path}")
if OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = OPENROUTER_API_KEY.strip()
    # Validate key format and length
    if not OPENROUTER_API_KEY.startswith('sk-') or len(OPENROUTER_API_KEY) < 20:
        raise OpenRouterAPIError(400, "Invalid or missing OPENROUTER_API_KEY. Ensure a valid key is set in .env.")
    print(f"DEBUG: Key loaded (Length: {len(OPENROUTER_API_KEY)}): {OPENROUTER_API_KEY[:6]}...{OPENROUTER_API_KEY[-4:]}")
else:
    raise OpenRouterAPIError(400, "OPENROUTER_API_KEY is missing. Please set it in .env.")

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

class OpenRouterAPIError(Exception):
    """Custom exception for OpenRouter API errors containing status code and details."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"OpenRouter API error {status_code}: {detail}")


async def call_openrouter(model: str, prompt: str, system_prompt: str = "") -> str:
    """Call OpenRouter API with specified model, handling errors and retries.

    Args:
        model: Model identifier string.
        prompt: User prompt.
        system_prompt: Optional system prompt.
    Returns:
        The generated content string.
    Raises:
        OpenRouterAPIError: For HTTP errors with details.
        RuntimeError: For missing or invalid API key.
    """
    # API key validation already performed during load
    print(f"DEBUG: Calling OpenRouter ({model}) with Key: {OPENROUTER_API_KEY[:6]}...")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "Vibe Coder",
    }

    messages = []
    if not system_prompt:
        system_prompt = "You are a helpful AI assistant."
    messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
    "model": model,
    "messages": messages
}

    # Simple retry logic: up to 2 attempts for transient network errors
    for attempt in range(1, 3):
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(OPENROUTER_BASE_URL, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
        except httpx.HTTPStatusError as exc:
            # Extract error details if available
            try:
                err_detail = exc.response.json().get("error", {}).get("message", exc.response.text)
            except Exception:
                err_detail = exc.response.text
            raise OpenRouterAPIError(exc.response.status_code, err_detail) from exc
        except (httpx.TransportError, httpx.RequestError) as exc:
            if attempt == 2:
                raise RuntimeError(f"Network error contacting OpenRouter after {attempt} attempts: {exc}")
            # else retry
            continue
        except Exception as e:
            traceback.print_exc()
            print(f"Error details: {str(e)}")
            raise OpenRouterAPIError(500, f"Unexpected error contacting OpenRouter: {e}")
