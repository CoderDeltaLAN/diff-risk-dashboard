from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .core import summarize_apv_json
from .report import to_markdown


def _exit_code(risk: str) -> int:
    return {"green": 0, "yellow": 1, "red": 2}.get(risk, 0)


def _print_table(summary: Mapping[str, Any]) -> None:
    by = summary.get("by_severity", {}) or {}
    print("Severity\tCount")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
        print(f"{sev}\t{by.get(sev, by.get(sev.lower(), 0))}")
    print(f"TOTAL\t{summary.get('total', 0)}")


def main() -> int:
    p = argparse.ArgumentParser(
        prog="diff_risk_dashboard", description="Diff Risk Dashboard (APV JSON -> summary)"
    )
    p.add_argument("input", help="Path o texto JSON de ai-patch-verifier")
    p.add_argument(
        "-f", "--format", choices=["table", "json", "md"], default="table", help="Formato de salida"
    )
    p.add_argument("-o", "--output", default="-", help="Archivo de salida; '-' = stdout")
    p.add_argument(
        "--no-exit-by-risk", action="store_true", help="No ajustar el exit code por nivel de riesgo"
    )
    args = p.parse_args()

    summary: Mapping[str, Any] = summarize_apv_json(args.input)
    out: str | None = None
    if args.format == "json":
        out = json.dumps(summary, indent=2)
    elif args.format == "md":
        out = to_markdown(summary)
    else:
        _print_table(summary)

    if out is not None:
        if args.output == "-":
            print(out)
        else:
            Path(args.output).write_text(out, encoding="utf-8")
            print(f"Wrote {args.output}", file=sys.stderr)

    risk = str(summary.get("risk", summary.get("risk_level", "green")))
    return 0 if args.no_exit_by_risk else _exit_code(risk)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
