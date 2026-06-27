from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: str  # high | medium | low
    confidence: float  # 0.0 - 1.0
    file: str
    line: int
    snippet: str
    message: str
    call_path: Optional[List[str]] = None

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "severity": self.severity,
            "confidence": round(self.confidence, 3),
            "file": self.file,
            "line": self.line,
            "snippet": self.snippet,
            "message": self.message,
            "call_path": self.call_path,
        }
