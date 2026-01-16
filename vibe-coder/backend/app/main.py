from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, files, terminal
import uvicorn
from loguru import logger

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
            # In a real implementation, we would hook this to the LLM interaction
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
