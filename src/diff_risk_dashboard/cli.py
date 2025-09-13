import argparse
import json
import sys
from pathlib import Path
from typing import Any

from rich.box import ROUNDED
from rich.console import Console
from rich.table import Table
from rich.text import Text

from .report import to_markdown

_SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]


def _risk_emoji(risk: str) -> str:
    return {"red": "🔴", "yellow": "🟡", "green": "🟢"}.get(risk, "🟢")


def _exit_code(risk: str) -> int:
    return {"green": 0, "yellow": 1, "red": 2}.get(risk, 0)


def _summarize(apv: dict) -> dict[str, int][str, int]:
    counts: dict[str, int][str, int] = {}
    for k, v in (apv.get("by_severity") or {}).items():
        counts[str(k).upper()] = int(v or 0)
    total = sum(counts.get(s, 0) for s in _SEVERITIES)
    worst = next((s for s in _SEVERITIES if counts.get(s, 0) > 0), "INFO")
    risk = str(apv.get("risk_level") or apv.get("risk") or "green").lower()
    return {"total": total, "by_severity": counts, "worst": worst, "risk_level": risk}


def _table_plain(summary: dict[str, Any]) -> str:
    counts: dict[str, int][str, int] = {s: int(summary["by_severity"].get(s, 0)) for s in _SEVERITIES}
    total = int(summary["total"])
    w_sev = max(len("Severity"), max(len(s) for s in _SEVERITIES))
    w_cnt = max(len("Count"), len(str(total)))
    header = f'{"Severity".ljust(w_sev)}  {"Count".rjust(w_cnt)}  {"Share":>5}'
    sep = f'{"-"*w_sev}  {"-"*w_cnt}  {"-"*5}'
    lines = [header, sep]
    for s in _SEVERITIES:
        n = counts.get(s, 0)
        pct = f"{(n/total*100):.0f}%" if total else "0%"
        lines.append(f"{s.ljust(w_sev)}  {str(n).rjust(w_cnt)}  {pct:>5}")
    lines.append(
        f'{"TOTAL".ljust(w_sev)}  {str(total).rjust(w_cnt)}  ' f'{"100%" if total else "0%":>5}'
    )
    return "\n".join(lines)


def _bar_plain(summary: dict[str, Any], width: int = 80) -> str:
    counts: dict[str, int][str, int] = {s: int(summary["by_severity"].get(s, 0)) for s in _SEVERITIES}
    total = int(summary["total"])
    maxc = max(counts.values()) if counts else 0
    bar_w = max(10, min(40, width - 24))
    lines = []
    for s in _SEVERITIES:
        n = counts.get(s, 0)
        w = 0 if maxc == 0 or n == 0 else max(1, round(n / maxc * bar_w))
        pct = f"{(n/total*100):.0f}%" if total else "0%"
        lines.append(f"{s:<8} {str(n).rjust(4)} {pct:>4}  " + ("█" * w))
    lines.append(f'{"TOTAL":<8} {str(total).rjust(4)} 100%')
    return "\n".join(lines)


def _table_rich(summary: dict[str, Any], width: int) -> Table:
    counts: dict[str, int][str, int] = {s: int(summary["by_severity"].get(s, 0)) for s in _SEVERITIES}
    total = int(summary["total"])
    worst = str(summary.get("worst", "UNKNOWN")).upper()
    risk = str(summary.get("risk", summary.get("risk_level", "green")) or "green").lower()
    emoji = _risk_emoji(risk)
    colors = {
        "CRITICAL": "bold bright_red",
        "HIGH": "red3",
        "MEDIUM": "yellow3",
        "LOW": "green3",
        "INFO": "cyan3",
    }
    maxc = max(counts.values()) if counts else 0
    bar_w = max(10, min(32, width - 42))

    def bar(n: int) -> str:
        if maxc == 0 or n == 0:
            return ""
        w = max(1, round(n / maxc * bar_w))
        return "█" * w

    title = Text.assemble(  # type: ignore[arg-type]
        ("Diff Risk Dashboard ", "bold"),
        (emoji + " ",),
        ("— Worst: ", "dim"),
        (worst, "bold"),
    )
    table = Table(
        title=title,
        header_style="bold cyan",
        box=ROUNDED,
        expand=True,
        show_lines=False,
        pad_edge=False,
    )
    table.add_column("Severity", justify="left", no_wrap=True)
    table.add_column("Count", justify="right")
    table.add_column("Share", justify="right")
    table.add_column("Bar", justify="left", no_wrap=True)
    for s in _SEVERITIES:
        n = counts.get(s, 0)
        pct = f"{(n/total*100):.0f}%" if total else "0%"
        col = colors.get(s, "")
        table.add_row(
            f"[{col}]{s}[/]",
            f"[{col}]{n}[/]",
            f"[{col}]{pct}[/]",
            f"[{col}]{bar(n)}[/]",
        )
    table.add_row(
        "[bold]TOTAL[/bold]",
        f"[bold]{total}[/bold]",
        "[bold]100%[/bold]" if total else "0%",
        "",
    )
    return table


def _bar_rich(summary: dict[str, Any], width: int) -> None:
    console = Console()
    counts: dict[str, int][str, int] = {s: int(summary["by_severity"].get(s, 0)) for s in _SEVERITIES}
    total = int(summary["total"])
    maxc = max(counts.values()) if counts else 0
    bar_w = max(10, min(40, width - 24))
    colors = {
        "CRITICAL": "bright_red",
        "HIGH": "red3",
        "MEDIUM": "yellow3",
        "LOW": "green3",
        "INFO": "cyan3",
    }
    for s in _SEVERITIES:
        n = counts.get(s, 0)
        w = 0 if maxc == 0 or n == 0 else max(1, round(n / maxc * bar_w))
        pct = f"{(n/total*100):.0f}%" if total else "0%"
        console.print(
            f"[{colors[s]}]{s:<8}[/] "
            f"[{colors[s]}]{n:>4} {pct:>4}[/]  "
            f"[{colors[s]}]{'█'*w}[/]"
        )
    console.print(f"[bold]TOTAL[/bold] {total:>4} 100%")


def main() -> int:
    p = argparse.ArgumentParser(
        prog="diff_risk_dashboard",
        description="Diff Risk Dashboard (APV JSON -> summary)",
    )
    p.add_argument("input", help="Path o texto JSON de ai-patch-verifier")
    p.add_argument(
        "-f",
        "--format",
        choices=["table", "json", "md", "bar"],
        default="table",
        help="Formato de salida",
    )
    p.add_argument(
        "-o",
        "--output",
        default="-",
        help="Archivo de salida; '-' = stdout",
    )
    p.add_argument(
        "--no-exit-by-risk",
        action="store_true",
        help="No ajustar el exit code por nivel de riesgo",
    )
    args = p.parse_args()

    apv = (
        json.loads(Path(args.input).read_text(encoding="utf-8"))
        if Path(args.input).exists()
        else json.loads(args.input)
    )
    summary = _summarize(apv)
    fmt = args.format.lower()
    out: str | None = None

    if fmt == "table":
        if args.output == "-" and sys.stdout.isatty():
            console = Console()
            console.print(_table_rich(summary, console.width))
            console.print(
                Text(
                    "Tip: usa  -f md  para reporte Markdown o  -f json  para máquinas.",
                    style="dim",
                )
            )
        else:
            out = _table_plain(summary) + "\n"
    elif fmt == "bar":
        if args.output == "-" and sys.stdout.isatty():
            _bar_rich(summary, Console().width)
        else:
            out = _bar_plain(summary) + "\n"
    elif fmt == "json":
        out = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    elif fmt == "md":
        out = to_markdown(summary) + "\n"
    else:
        out = _table_plain(summary) + "\n"

    if out is not None:
        if args.output == "-":
            sys.stdout.write(out)
        else:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(out, encoding="utf-8")
            print(f"Wrote {args.output}")

    if not args.no_exit_by_risk:
        return _exit_code(str(summary.get("risk", summary.get("risk_level", "green"))).lower())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
