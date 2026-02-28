from datetime import datetime
from typing import Dict, Any


class ToolingLayer:
    """Cross-cutting tooling helpers (observability/trace metadata)."""

    @staticmethod
    def build_trace(event: str) -> Dict[str, Any]:
        return {
            "event": event,
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "service": "supply-chain-ai",
        }
