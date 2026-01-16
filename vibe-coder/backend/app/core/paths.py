import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
WORKSPACE_DIR = BASE_DIR / "workspace"
PROJECTS_DIR = WORKSPACE_DIR / "projects"
REPORTS_DIR = WORKSPACE_DIR / "reports"

def get_project_path(project_name: str) -> Path:
    return PROJECTS_DIR / project_name
