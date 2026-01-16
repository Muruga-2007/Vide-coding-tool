from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.core.config import settings
from app.services import llm_manager, prompt_builder, context_builder

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    project_path: Optional[str] = None
    history: Optional[List[Dict[str, str]]] = None

@router.post("/query")
async def chat_query(request: ChatRequest):
    # 1. Retrieve Context (only if index exists/project path provided)
    # In a real scenario, we'd ensure index is loaded for this project
    context_files = context_builder.retrieve_context(request.message)
    
    # 2. Build Prompt
    system_prompt = prompt_builder.build_system_prompt(context_files)
    messages = llm_manager.create_messages(system_prompt, request.message, request.history)
    
    # 3. Get Response
    response = await llm_manager.get_response(messages)
    
    return {"response": response, "context": context_files}
