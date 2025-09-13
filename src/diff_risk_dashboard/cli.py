from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Literal, TypedDict

from .core import summarize_apv_json
from .report import to_markdown


class Summary(TypedDict):
    total: int
    worst: str
    risk: Literal["red", "yellow", "green"]
    by_severity: dict


def _print_table(summary: Summary) -> None:
    by = summary["by_severity"]
    print("Severity\tCount")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
        print(f"{sev}\t{by.get(sev, by.get(sev.lower(), 0))}")
    print(f"TOTAL\t{summary['total']}")


def _exit_code(risk: str) -> int:
    # 0=green, 1=yellow, 2=red
    return {"green": 0, "yellow": 1, "red": 2}.get(risk, 0)


def main() -> int:
    p = argparse.ArgumentParser(prog="diff-risk")
    p.add_argument("input", help="Path o texto JSON de APV (ai-patch-verifier)")
    p.add_argument(
        "-f",
        "--format",
        choices=["table", "json", "md"],
        default="table",
        help="Formato de salida (por defecto: table)",
    )
    p.add_argument(
        "-o", "--output", default="-", help="Archivo de salida; '-' = stdout (por defecto)"
    )
    p.add_argument(
        "--no-exit-by-risk", action="store_true", help="No ajustar el exit code por nivel de riesgo"
    )
    args = p.parse_args()

    summary: Summary = summarize_apv_json(args.input)  # path o texto
    out = ""
    if args.format == "json":
        out = json.dumps(summary, indent=2)
    elif args.format == "md":
        out = to_markdown(summary)
    else:
        _print_table(summary)

    if args.format in {"json", "md"}:
        if args.output == "-":
            print(out)
        else:
            Path(args.output).write_text(out, encoding="utf-8")
            print(f"Wrote {args.output}", file=sys.stderr)

    if not args.no - exit - by - risk:
        return _exit_code(summary["risk"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
