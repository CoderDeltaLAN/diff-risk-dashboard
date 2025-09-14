from __future__ import annotations

import json
from collections.abc import Mapping
from typing import TypedDict


class SeveritySummary(TypedDict):
    total: int
    by_severity: Mapping[str, int]


def to_markdown(summary: SeveritySummary) -> str:
    lines = [
        "| Severity | Count |",
        "|---|---|",
        f"| critical | {summary['by_severity'].get('critical', 0)} |",
        f"| high | {summary['by_severity'].get('high', 0)} |",
        f"| total | {summary['total']} |",
    ]
    return "\n".join(lines) + "\n"


def to_json(summary: SeveritySummary) -> str:
    payload = {
        "total": summary["total"],
        "by_severity": dict(summary["by_severity"]),
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
