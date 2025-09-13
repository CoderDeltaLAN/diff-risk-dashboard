from __future__ import annotations
import argparse
from rich.console import Console
from rich.table import Table
from .core import summarize_apv_json

def main() -> None:
    parser = argparse.ArgumentParser(description="Diff Risk Dashboard (CLI)")
    parser.add_argument("json_path", help="Path to ai-patch-verifier JSON report")
    args = parser.parse_args()

    summary = summarize_apv_json(args.json_path)
    console = Console()
    table = Table(title="PR Risk Exposure")
    table.add_column("Severity", justify="left")
    table.add_column("Count", justify="right")

    for sev in ["high", "medium", "low"]:
        table.add_row(sev.capitalize(), str(summary["by_severity"][sev]))

    console.print(table)
    console.print(f"[bold]Total findings:[/bold] {summary['total']}")
