from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Literal, TypedDict, cast

Severity = Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


class Finding(TypedDict, total=False):
    severity: Severity
    title: str
    score: float


class Summary(TypedDict):
    total: int
    by_severity: dict[str, int]
    worst: Severity
    risk_level: Literal["red", "yellow", "green"]


_SEV_ORDER: dict[Severity, int] = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
    "INFO": 0,
}


def _norm_sev(s: str | None) -> Severity:
    if not s:
        return "INFO"
    s = s.upper().strip()
    if s in _SEV_ORDER:
        return cast(Severity, s)
    if s in {"CRIT"}:
        return "CRITICAL"
    if s in {"MED", "MODERATE"}:
        return "MEDIUM"
    return "INFO"


def _iter_findings(obj: Any) -> Iterable[Finding]:
    # APV: {"findings":[...]} o lista directa
    if isinstance(obj, dict):
        cand = obj.get("findings", obj.get("results", []))
        if isinstance(cand, list):
            for x in cand:
                if isinstance(x, dict):
                    yield cast(Finding, x)
        return
    if isinstance(obj, list):
        for x in obj:
            if isinstance(x, dict):
                yield cast(Finding, x)


def summarize(obj: Any) -> Summary:
    counts: dict[str, int] = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    total = 0
    for f in _iter_findings(obj):
        sev = _norm_sev(cast(str | None, f.get("severity")))
        counts[sev] += 1
        total += 1

    worst: Severity = "INFO"
    if counts["CRITICAL"] > 0:
        worst = "CRITICAL"
    elif counts["HIGH"] > 0:
        worst = "HIGH"
    elif counts["MEDIUM"] > 0:
        worst = "MEDIUM"
    elif counts["LOW"] > 0:
        worst = "LOW"

    if worst in {"CRITICAL", "HIGH"}:
        risk: Literal["red", "yellow", "green"] = "red"
    elif worst == "MEDIUM":
        risk = "yellow"
    else:
        risk = "green"

    return {
        "total": total,
        "by_severity": {
            "CRITICAL": counts["CRITICAL"],
            "HIGH": counts["HIGH"],
            "MEDIUM": counts["MEDIUM"],
            "LOW": counts["LOW"],
            "INFO": counts["INFO"],
        },
        "worst": worst,
        "risk_level": risk,
    }


def summarize_apv_json(text_or_path: str | bytes) -> Summary:
    """Acepta JSON (str/bytes) o una ruta a archivo JSON."""
    if isinstance(text_or_path, bytes):
        payload = text_or_path.decode("utf-8", errors="strict")
    else:
        p = Path(text_or_path)
        payload = p.read_text(encoding="utf-8") if p.exists() else text_or_path
    data = json.loads(payload)
    return summarize(data)
