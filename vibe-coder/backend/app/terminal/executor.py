import subprocess
import asyncio
from typing import Tuple
from loguru import logger

class TerminalExecutor:
    async def run_command(self, command: str, cwd: str = ".") -> Tuple[str, str, int]:
        """
        Executes a shell command and returns (stdout, stderr, return_code).
        """
        logger.info(f"Executing command: {command} in {cwd}")
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            stdout_decoded = stdout.decode().strip()
            stderr_decoded = stderr.decode().strip()
            
            return stdout_decoded, stderr_decoded, process.returncode
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return "", str(e), -1
