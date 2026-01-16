import sys
import os
from pathlib import Path
import asyncio
from loguru import logger

# Add app to path
sys.path.append(os.path.join(os.getcwd(), 'app'))

# Mock Settings
os.environ["PROJECT_NAME"] = "Vibe Coder Test"

try:
    from app.repo.scanner import RepoScanner
    from app.repo.diff_manager import DiffManager
    from app.terminal.executor import TerminalExecutor
except ImportError as e:
    logger.error(f"Import Error: {e}")
    sys.exit(1)

async def test_backend():
    logger.info("Starting Backend Verification...")
    
    # 1. Test Repo Scanner
    logger.info("Testing Repo Scanner...")
    # Use the backend directory itself as a test case
    test_path = Path(os.getcwd()) / "app"
    scanner = RepoScanner(str(test_path))
    files = scanner.scan()
    if not files:
        logger.error("Repo Scanner failed: No files found")
    else:
        logger.info(f"Repo Scanner Success: Found {len(files)} files")

    # 2. Test Diff Manager
    logger.info("Testing Diff Manager...")
    diff_manager = DiffManager(str(Path(os.getcwd()).parent / "workspace"))
    # Test path traversal protection
    res = diff_manager.apply_diff("../../../secret.txt", "hacked")
    if not res["success"] and "Invalid path" in res.get("error", ""):
        logger.info("Diff Manager Security Success: Path traversal blocked")
    else:
        logger.warning(f"Diff Manager Security Warning: {res}")

    # 3. Test Terminal Executor
    logger.info("Testing Terminal Executor...")
    executor = TerminalExecutor()
    stdout, stderr, code = await executor.run_command("echo 'Hello Vibe'", cwd=".")
    if "Hello Vibe" in stdout and code == 0:
        logger.info("Terminal Executor Success")
    else:
        logger.error(f"Terminal Executor Failed: {stderr}")

    logger.info("Backend Verification Complete.")

if __name__ == "__main__":
    asyncio.run(test_backend())
