import sys
from pathlib import Path

# Fix path to allow running directly: python main.py
if __name__ == "__main__":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from loguru import logger
from typing import List

# Import app modules after path fix
try:
    from app.api import chat, files, terminal
    from app.services import llm_manager, context_builder, prompt_builder
except ImportError as e:
    # Fallback/Error logging if path setup failed
    logger.error(f"Failed to import app modules: {e}")
    raise e

app = FastAPI(title="Vibe Coder API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
app.include_router(terminal.router, prefix="/api/v1/terminal", tags=["terminal"])

@app.get("/")
async def root():
    return {"message": "Vibe Coder API is running"}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")
    try:
        while True:
            data = await websocket.receive_text()
            
            # 1. Retrieve Context
            context_files = context_builder.retrieve_context(data)
            
            # 2. Build Prompt
            system_prompt = prompt_builder.build_system_prompt(context_files)
            messages = llm_manager.create_messages(system_prompt, data)
            
            # 3. Stream Response
            async for chunk in llm_manager.stream_response(messages):
                await websocket.send_text(chunk)
                
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    logger.info("Starting Vibe Coder Backend...")
    # Using reload=True with a string requires the module to be importable
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
