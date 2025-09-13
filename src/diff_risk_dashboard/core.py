from __future__ import annotations

import json
from collections.abc import Iterable
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
    # APV: {"findings":[{...}]} o lista directa
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
    counts: dict[str, int] = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "INFO": 0,
    }
    total = 0
    for f in _iter_findings(obj):
        sev = _norm_sev(cast(str | None, f.get("severity")))
        counts[sev] += 1
        total += 1

    # peor severidad (evita E701)
    worst: Severity = "INFO"
    if counts["CRITICAL"] > 0:
        worst = "CRITICAL"
    elif counts["HIGH"] > 0:
        worst = "HIGH"
    elif counts["MEDIUM"] > 0:
        worst = "MEDIUM"
    elif counts["LOW"] > 0:
        worst = "LOW"

    # nivel de riesgo
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


def summarize_apv_json(text: str | bytes) -> Summary:
    """Compat para tests de humo: recibe JSON en texto y devuelve Summary."""
    data = json.loads(text)
    return summarize(data)
