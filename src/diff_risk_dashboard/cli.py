from __future__ import annotations

import argparse
import json
import pathlib
import sys
from collections.abc import Mapping
from typing import Any, cast

from .report import SeveritySummary, to_json, to_markdown


def _extract_findings(data: object) -> list[Mapping[str, Any]]:
    if isinstance(data, list):
        return [cast(Mapping[str, Any], x) for x in data]
    if isinstance(data, dict):
        maybe = data.get("findings")
        if isinstance(maybe, list):
            return [cast(Mapping[str, Any], x) for x in maybe]
    return []


def summarize_apv_json(data: object) -> SeveritySummary:
    findings = _extract_findings(data)
    counts: dict[str, int] = {}
    for f in findings:
        sev = str(f.get("severity", "unknown")).lower()
        counts[sev] = counts.get(sev, 0) + 1
    return {"total": len(findings), "by_severity": cast(Mapping[str, int], counts)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="diff-risk")
    parser.add_argument("input", help="APV JSON file")
    parser.add_argument("-f", "--format", choices=["md", "json"], default="md")
    parser.add_argument("-o", "--output", help="Output path", default="-")
    args = parser.parse_args(argv)

    data = json.loads(pathlib.Path(args.input).read_text(encoding="utf-8"))
    summary = summarize_apv_json(data)
    rendered = to_markdown(summary) if args.format == "md" else to_json(summary) + "\n"

    if args.output == "-" or args.output == "":
        sys.stdout.write(rendered)
    else:
        pathlib.Path(args.output).write_text(rendered, encoding="utf-8")

    try:
        from rich.console import Console
        from rich.text import Text

        Console().print(Text.assemble("Wrote ", (str(args.output), "bold")))
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
