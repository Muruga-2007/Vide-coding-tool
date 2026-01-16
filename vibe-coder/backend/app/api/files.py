from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from typing import List, Optional
from app.repo.scanner import RepoScanner
from app.services import embedding_manager 
from loguru import logger
import os
from pathlib import Path

router = APIRouter()

class IndexRequest(BaseModel):
    path: str

@router.post("/index")
async def index_project(request: IndexRequest):
    try:
        scanner = RepoScanner(request.path)
        files = scanner.scan()
        embedding_manager.create_index(files)
        return {"message": f"Indexed {len(files)} files", "files_count": len(files)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_files(path: str):
    """
    List files in the directory for the frontend file explorer.
    """
    try:
        scanner = RepoScanner(path)
        # We can reuse the scanner logic or build a simple tree builder
        # For now, let's just use os.walk but return a tree structure
        directory_structure = []
        root_path = Path(path)
        
        if not root_path.exists():
             raise HTTPException(status_code=404, detail="Path not found")

        # Simplified flat list for now, ideally return a tree
        for root, dirs, files in os.walk(root_path):
            if scanner._should_ignore(Path(root)):
                continue
                
            rel_root = Path(root).relative_to(root_path)
            
            for f in files:
                if scanner._should_ignore(Path(root) / f): 
                    continue
                directory_structure.append({
                    "path": str(rel_root / f),
                    "name": f,
                    "type": "file"
                })
            
            for d in dirs:
                if not scanner._should_ignore(Path(root) / d):
                    directory_structure.append({
                        "path": str(rel_root / d),
                        "name": d,
                        "type": "directory"
                    })
                    
        return directory_structure
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=str(e))

