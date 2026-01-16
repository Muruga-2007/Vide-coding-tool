import difflib
import os
from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger
import git
from datetime import datetime

class DiffManager:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.repo = self._init_git_repo()

    def _init_git_repo(self) -> Optional[git.Repo]:
        try:
            if not (self.root_path / '.git').exists():
                 logger.info(f"Initializing git repo in {self.root_path}")
                 return git.Repo.init(self.root_path)
            return git.Repo(self.root_path)
        except Exception as e:
            logger.error(f"Failed to init git repo: {e}")
            return None

    def create_snapshot(self, message: str = "AI Snapshot"):
        if not self.repo:
            return
        try:
            # Check for changes
            if self.repo.is_dirty(untracked_files=True):
                self.repo.git.add([str(self.root_path)])
                self.repo.index.commit(f"{message} - {datetime.now().isoformat()}")
                logger.info("Created git snapshot")
        except Exception as e:
            logger.error(f"Snapshot failed: {e}")

    def generate_diff(self, file_path: str, original_content: str, new_content: str) -> str:
        diff = difflib.unified_diff(
            original_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=file_path,
            tofile=file_path,
        )
        return "".join(diff)

    def apply_diff(self, file_path: str, new_content: str) -> Dict:
        """
        Applies changes to a file safely.
        """
        full_path = self.root_path / file_path
        
        # Security check: Path traversal
        try:
            full_path.resolve().relative_to(self.root_path.resolve())
        except ValueError:
             return {"success": False, "error": "Invalid path"}

        try:
            # 1. Snapshot before write
            self.create_snapshot(f"Pre-change: {file_path}")

            # 2. Write file
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # 3. Snapshot after write
            self.create_snapshot(f"Post-change: {file_path}")
            
            return {"success": True, "message": f"Updated {file_path}"}
        except Exception as e:
            logger.error(f"Failed to apply diff: {e}")
            return {"success": False, "error": str(e)}
