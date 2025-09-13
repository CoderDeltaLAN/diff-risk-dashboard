from __future__ import annotations

import argparse
import json
import os
from collections.abc import Iterable, Mapping
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .report import SEVERITIES, Summary, to_markdown

SEV_ORDER: tuple[str, ...] = tuple(SEVERITIES)
SEV_TO_COLOR: dict[str, str] = {
    "CRITICAL": "bold bright_red",
    "HIGH": "red3",
    "MEDIUM": "yellow3",
    "LOW": "sky_blue3",
    "INFO": "green3",
}


def _normalize(sev: str) -> str:
    return sev.strip().upper()


def _count_by_severity_from_list(
    items: Iterable[Mapping[str, Any]],
) -> dict[str, int]:
    counts: dict[str, int] = {k: 0 for k in SEVERITIES}
    for it in items:
        raw = it.get("severity") or it.get("level") or ""
        sev = _normalize(str(raw))
        if sev in counts:
            counts[sev] += 1
    return counts


def _build_summary(apv_obj: object) -> Summary:
    # Soporta:
    # 1) {"by_severity": {"HIGH": 1, ...}}
    # 2) [{"severity": "HIGH"}, ...] o en "findings"/"items"
    counts: dict[str, int] = {k: 0 for k in SEVERITIES}

    if isinstance(apv_obj, Mapping):
        bs = apv_obj.get("by_severity")
        if isinstance(bs, Mapping):
            for k, v in bs.items():
                kk = _normalize(str(k))
                if kk in counts:
                    try:
                        counts[kk] += int(v)  # type: ignore[arg-type]
                    except Exception:
                        pass
        items = apv_obj.get("findings") or apv_obj.get("items")
        if isinstance(items, list) and not any(counts.values()):
            counts = _count_by_severity_from_list(items)  # type: ignore[arg-type]
    elif isinstance(apv_obj, list):
        counts = _count_by_severity_from_list(apv_obj)  # type: ignore[arg-type]

    total = sum(counts.values())

    worst = "INFO"
    for sev in SEV_ORDER:
        if counts.get(sev, 0) > 0:
            worst = sev
            break

    if worst in ("CRITICAL", "HIGH"):
        risk = "red"
    elif worst in ("MEDIUM", "LOW"):
        risk = "yellow"
    else:
        risk = "green"

    return Summary(total=total, by_severity=counts, worst=worst, risk_level=risk)


def _load_input(s: str) -> object:
    if os.path.isfile(s):
        with open(s, encoding="utf-8") as fh:
            return json.load(fh)
    if s.lstrip().startswith("{") or s.lstrip().startswith("["):
        return json.loads(s)
    raise SystemExit(f"✗ Not found and not JSON: {s}")


def _render_table(summary: Summary, console: Console) -> None:
    if summary.total == 0:
        console.print(
            Panel.fit(
                "✅ No findings",
                border_style="green",
                title="Diff Risk Dashboard",
            )
        )
        return

    if summary.risk_level == "red":
        title_dot = "🔴"
    elif summary.risk_level == "yellow":
        title_dot = "🟡"
    else:
        title_dot = "🟢"

    table = Table(
        title=f"Diff Risk Dashboard {title_dot} — Worst: {summary.worst}",
        title_justify="center",
        show_header=True,
        header_style="bold",
        expand=True,
    )
    table.add_column("Severity")
    table.add_column("Count", justify="right")
    table.add_column("Share", justify="right")
    table.add_column("Bar")

    total = max(1, summary.total)
    bar_width = max(10, min(48, console.size.width - 60))

    for sev in SEVERITIES:
        c = summary.by_severity.get(sev, 0)
        share = int(round((c / total) * 100))
        blocks = "█" * int(round((share / 100) * bar_width))
        style = SEV_TO_COLOR.get(sev, "")
        table.add_row(sev, str(c), f"{share}%", f"[{style}]{blocks}[/{style}]")

    table.add_row("TOTAL", str(summary.total), "100%" if summary.total else "0%", "")
    console.print(table)
    console.print(
        "Tip: usa  -f md  para reporte Markdown o  -f json  para máquinas.",
        style="dim",
    )


def _render_bars(summary: Summary) -> None:
    total = max(1, summary.total)
    for sev in SEVERITIES + ["TOTAL"]:
        if sev == "TOTAL":
            c = summary.total
            pct = 100 if summary.total else 0
        else:
            c = summary.by_severity.get(sev, 0)
            pct = int(round((c / total) * 100))
        print(f"{sev:<10} {c:>4} {pct:>3}%  {'█' * int(pct/4)}")


def main() -> None:
    desc = "Diff Risk Dashboard (APV JSON -> summary)"
    p = argparse.ArgumentParser(prog="diff_risk_dashboard", description=desc)
    p.add_argument("input", help="File path or inline JSON")
    p.add_argument(
        "-f",
        "--format",
        choices=("table", "json", "md", "bar"),
        default="table",
        help="Output format",
    )
    p.add_argument("-o", "--output", default="-", help="Output file; '-' = stdout")
    p.add_argument(
        "--no-exit-by-risk",
        action="store_true",
        help="Do not set exit code by risk level",
    )
    args = p.parse_args()

    apv_obj = _load_input(args.input)
    summary = _build_summary(apv_obj)

    if args.format == "json":
        payload = {
            "total": summary.total,
            "by_severity": summary.by_severity,
            "worst": summary.worst,
            "risk_level": summary.risk_level,
        }
        out = json.dumps(payload, ensure_ascii=False, indent=2)
        if args.output == "-" or not args.output:
            print(out)
        else:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(out + "\n")

    elif args.format == "md":
        md = to_markdown(summary)
        if args.output == "-" or not args.output:
            print(md)
        else:
            with open(args.output, "w", encoding="utf-8") as fh:
                fh.write(md)

    elif args.format == "bar":
        _render_bars(summary)

    else:  # table
        console = Console(force_jupyter=False, force_terminal=None, soft_wrap=False)
        _render_table(summary, console)

    if not args.no_exit_by_risk:
        if summary.risk_level == "red":
            raise SystemExit(2)
        if summary.risk_level == "yellow":
            raise SystemExit(1)
    raise SystemExit(0)


if __name__ == "__main__":
    main()
