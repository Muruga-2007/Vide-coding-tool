import os
from pathlib import Path
from typing import List, Dict, Optional
import pathspec
from loguru import logger

class RepoScanner:
    SUPPORTED_EXTENSIONS = {
        '.py', '.js', '.ts', '.tsx', '.jsx', '.json', '.md', '.html', '.css',
        '.java', '.c', '.cpp', '.rs', '.go', '.yml', '.yaml', '.sql', '.sh'
    }

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.gitignore_spec = self._load_gitignore()

    def _load_gitignore(self) -> Optional[pathspec.PathSpec]:
        gitignore_path = self.root_path / '.gitignore'
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    return pathspec.PathSpec.from_lines('gitwildmatch', f)
            except Exception as e:
                logger.error(f"Error reading .gitignore: {e}")
        return None

    def _should_ignore(self, file_path: Path) -> bool:
        # Relative path for matching
        try:
            rel_path = file_path.relative_to(self.root_path).as_posix()
        except ValueError:
            return True # Should not happen if walking inside root
        
        # Always ignore common junk directories
        parts = file_path.parts
        if any(part in {'.git', 'node_modules', '__pycache__', 'venv', '.env', '.idea', '.vscode'} for part in parts):
            return True

        if self.gitignore_spec and self.gitignore_spec.match_file(rel_path):
            return True
        
        return False

    def scan(self) -> List[Dict]:
        indexed_files = []
        if not self.root_path.exists():
            logger.error(f"Root path {self.root_path} does not exist")
            return []

        for root, dirs, files in os.walk(self.root_path):
            # Modify dirs in-place to skip ignored directories early
            dirs[:] = [d for d in dirs if not self._should_ignore(Path(root) / d)]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix not in self.SUPPORTED_EXTENSIONS:
                    continue
                
                if self._should_ignore(file_path):
                    continue

                try:
                    # Using errors='ignore' to skip non-utf8 files
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    indexed_files.append({
                        "path": str(file_path.relative_to(self.root_path)),
                        "content": content,
                        "size": file_path.stat().st_size
                    })
                except Exception as e:
                    logger.error(f"Error reading {file_path}: {e}")
        
        logger.info(f"Scanned {len(indexed_files)} files in {self.root_path}")
        return indexed_files
