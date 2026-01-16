import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from app.core.paths import REPORTS_DIR

class ErrorDetector:
    def __init__(self):
        self.errors_dir = REPORTS_DIR / "errors"
        self.errors_dir.mkdir(parents=True, exist_ok=True)

    def analyze_output(self, stderr: str, context: str = "") -> Optional[Dict]:
        """
        Analyzes stderr to detect errors and saves a report.
        """
        if not stderr:
            return None

        # Simple heuristic for now - real implementation would be smarter
        error_type = "UnknownError"
        if "ImportError" in stderr or "ModuleNotFoundError" in stderr:
            error_type = "ImportError"
        elif "SyntaxError" in stderr:
            error_type = "SyntaxError"
        elif "TypeError" in stderr:
            error_type = "TypeError"
        elif "NameError" in stderr:
            error_type = "NameError"
        else:
             # If obscure, maybe not an error we can categorize easily, but still log
             if "Error:" not in stderr and "Exception" not in stderr:
                 # Check if it looks like an error
                 return None
             error_type = "RuntimeError"

        report = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "description": stderr[:500], # Truncate for summary
            "full_trace": stderr,
            "context": context
        }
        
        self._save_report(report)
        return report

    def _save_report(self, report: Dict):
        filename = f"error_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_{report['id'][:8]}.json"
        with open(self.errors_dir / filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
