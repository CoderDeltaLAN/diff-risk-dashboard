from __future__ import annotations

from typing import Any

_SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


def _norm_counts(summary: dict[str, Any]) -> dict[str, int]:
    src = summary.get("by_severity") or {}
    by = {str(k).upper(): int(v) for k, v in src.items()}
    return {s: int(by.get(s, 0)) for s in _SEVERITIES}


def to_markdown(summary: dict[str, Any]) -> str:
    counts = _norm_counts(summary)
    total = int(summary.get("total", sum(counts.values())))
    worst = str(summary.get("worst") or summary.get("risk_level") or "INFO").upper()
    risk = str(summary.get("risk_level", "green") or "green").lower()
    emoji = {"red": "🔴", "yellow": "🟡", "green": "🟢"}.get(risk, "🟢")

    zero = total == 0 or sum(counts.values()) == 0
    if zero:
        # Zero-state: limpio y profesional
        return "\n".join(
            [
                f"# Diff Risk Dashboard {emoji} — No findings",
                "",
                "> ✅ No findings. All severities are 0.",
                "",
                "| Severity | Count |",
                "|---|---:|",
                "| **TOTAL** | **0** |",
                "",
            ]
        )

    # Caso normal: tabla completa (compatibilidad con tests/README)
    lines = [
        f"# Diff Risk Dashboard {emoji} — Worst: **{worst}**",
        "",
        "| Severity | Count |",
        "|---|---:|",
    ]
    for sev in _SEVERITIES:
        lines.append(f"| {sev} | {counts.get(sev, 0)} |")
    lines.append(f"| **TOTAL** | **{total}** |")
    lines.append("")
    return "\n".join(lines)


# Alias de compatibilidad
render_markdown = to_markdown
