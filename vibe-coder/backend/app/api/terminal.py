from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.terminal.executor import TerminalExecutor

router = APIRouter()
executor = TerminalExecutor()

class CommandRequest(BaseModel):
    command: str
    cwd: str = "."

@router.post("/run")
async def run_command(request: CommandRequest):
    stdout, stderr, return_code = await executor.run_command(request.command, request.cwd)
    return {
        "stdout": stdout,
        "stderr": stderr,
        "return_code": return_code
    }
