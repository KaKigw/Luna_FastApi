from datetime import datetime, timezone
import json
import os

REPORT_FILE = "reports.jsonl"

def report_issue(user_id: str, query: str, classification: str, feedback: str):
    """
    feedback ∈ {"helpful", "unhelpful", "unsafe"}
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "classification": classification,
        "feedback": feedback,
        "query": query
    }
    os.makedirs("logs", exist_ok=True)
    with open(os.path.join("logs", REPORT_FILE), "a") as f:
        f.write(json.dumps(entry) + "\n")
