from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .core import summarize

def _print_table(summary: dict) -> None:
    bs = summary["by_severity"]
    rows = [
        ("CRITICAL", bs["CRITICAL"]),
        ("HIGH",     bs["HIGH"]),
        ("MEDIUM",   bs["MEDIUM"]),
        ("LOW",      bs["LOW"]),
        ("INFO",     bs["INFO"]),
    ]
    print("\n=== Diff Risk Summary ===")
    print(f"Total findings: {summary['total']}")
    print("Severity counts:")
    w = max(len(r[0]) for r in rows)
    for name, cnt in rows:
        print(f"  {name:<{w}} : {cnt}")
    print(f"Worst severity : {summary['worst']}")
    print(f"Risk level     : {summary['risk_level']}\n")

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Diff Risk Dashboard (APV JSON -> summary)")
    p.add_argument("apv_json", help="Path to ai-patch-verifier JSON (list or {findings:[...]})")
    args = p.parse_args(argv)
    data = json.loads(Path(args.apv_json).read_text(encoding="utf-8"))
    sm = summarize(data)
    _print_table(sm)
    return 2 if sm["risk_level"]=="red" else (1 if sm["risk_level"]=="yellow" else 0)

if __name__ == "__main__":
    sys.exit(main())
