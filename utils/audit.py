import json
import os
from datetime import datetime
from typing import List, Dict, Any

class Auditor:
    def __init__(self, log_file="audit_log.json"):
        self.log_file = log_file
        self.logs = []

    def log_event(self, ticket_id: str, event_type: str, data: Any):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "ticket_id": ticket_id,
            "type": event_type,
            "data": data
        }
        self.logs.append(log_entry)
        print(f"[{ticket_id}] {event_type}: {str(data)[:100]}...")

    def save(self):
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=2)

    def get_ticket_logs(self, ticket_id: str) -> List[Dict]:
        return [log for log in self.logs if log["ticket_id"] == ticket_id]
