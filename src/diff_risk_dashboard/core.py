from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Literal, TypedDict, cast

Severity = Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


class Finding(TypedDict, total=False):
    severity: str
    predicted_risk: str
    title: str
    score: float


class Summary(TypedDict):
    total: int
    by_severity: dict[str, int]  # incluye claves lower y UPPER
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
    s = s.strip().upper()
    if s in _SEV_ORDER:
        return s  # type: ignore[return-value]
    if s in {"CRIT"}:
        return "CRITICAL"
    if s in {"MED", "MODERATE"}:
        return "MEDIUM"
    if s in {"WARN", "WARNING"}:
        return "LOW"
    return "INFO"


def _extract_raw_sev(f: Finding) -> str | None:
    return f.get("severity") or f.get("predicted_risk")


def _iter_findings(obj: Any) -> Iterable[Finding]:
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
    counts_uc: dict[Severity, int] = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
    total = 0
    for f in _iter_findings(obj):
        sev = _norm_sev(_extract_raw_sev(f))
        counts_uc[sev] += 1
        total += 1

    worst: Severity = "INFO"
    if counts_uc["CRITICAL"] > 0:
        worst = "CRITICAL"
    elif counts_uc["HIGH"] > 0:
        worst = "HIGH"
    elif counts_uc["MEDIUM"] > 0:
        worst = "MEDIUM"
    elif counts_uc["LOW"] > 0:
        worst = "LOW"

    if worst in {"CRITICAL", "HIGH"}:
        risk: Literal["red", "yellow", "green"] = "red"
    elif worst == "MEDIUM":
        risk = "yellow"
    else:
        risk = "green"

    by_lc = {
        "critical": counts_uc["CRITICAL"],
        "high": counts_uc["HIGH"],
        "medium": counts_uc["MEDIUM"],
        "low": counts_uc["LOW"],
        "info": counts_uc["INFO"],
    }
    by_uc = {
        "CRITICAL": counts_uc["CRITICAL"],
        "HIGH": counts_uc["HIGH"],
        "MEDIUM": counts_uc["MEDIUM"],
        "LOW": counts_uc["LOW"],
        "INFO": counts_uc["INFO"],
    }
    by_sev: dict[str, int] = {**by_lc, **by_uc}
    return {"total": total, "by_severity": by_sev, "worst": worst, "risk_level": risk}


def summarize_apv_json(text_or_path: str | bytes) -> Summary:
    """Acepta JSON (str/bytes) o ruta a archivo JSON."""
    if isinstance(text_or_path, bytes):
        payload = text_or_path.decode("utf-8", errors="strict")
    else:
        p = Path(text_or_path)
        payload = p.read_text(encoding="utf-8") if p.exists() else text_or_path
    data = json.loads(payload)
    return summarize(data)
