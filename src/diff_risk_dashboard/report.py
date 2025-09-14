from __future__ import annotations

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
    import json

    by_sev = dict(summary["by_severity"])
    payload = {"total": summary["total"], "by_severity": by_sev}
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
