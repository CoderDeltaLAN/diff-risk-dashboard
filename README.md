# ⭐ diff-risk-dashboard — APV → Risk Summary (Python CLI)

A lean, production-grade **Python CLI** that ingests **ai-patch-verifier (APV)** JSON and outputs a clear **risk summary** in **JSON** or **Markdown**.

<div align="center">

[![Manual](https://img.shields.io/badge/Manual-User%20Guide-blue?style=for-the-badge)](docs/MANUAL.md)

<br/>

[![CI / build](https://github.com/CoderDeltaLAN/diff-risk-dashboard/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/CoderDeltaLAN/diff-risk-dashboard/actions/workflows/build.yml)
[![CodeQL Analysis](https://github.com/CoderDeltaLAN/diff-risk-dashboard/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/CoderDeltaLAN/diff-risk-dashboard/actions/workflows/codeql.yml)
[![Release](https://img.shields.io/github/v/release/CoderDeltaLAN/diff-risk-dashboard?display_name=tag)](https://github.com/CoderDeltaLAN/diff-risk-dashboard/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

---
## Repo layout

```text
.
├── examples/
│   └── sample_apv.json           # APV sample for demos/tests
├── src/diff_risk_dashboard/
│   ├── __main__.py               # module entry
│   ├── cli.py                    # CLI
│   ├── core.py                   # summarization logic
│   └── report.py                 # Markdown generator
├── tests/                        # pytest
└── .github/workflows/            # CI + CodeQL + Release Drafter
```

---

## 🚀 Quick Start

```bash
# 1) Clone
git clone https://github.com/CoderDeltaLAN/diff-risk-dashboard.git
cd diff-risk-dashboard

# 2) Install (isolated venv recommended)
python -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
python -m pip install .

# 3) Use the CLI
# Table-like Markdown to file
diff-risk examples/sample_apv.json -f md -o report.md
# JSON to stdout
diff-risk examples/sample_apv.json -f json
```

### CLI usage

```bash
diff-risk -h
```

```
usage: diff-risk [-h] [-f {md,json}] [-o OUTPUT] input

Diff Risk Dashboard (APV JSON -> summary)

positional arguments:
  input                 Path to ai-patch-verifier JSON

options:
  -h, --help            show this help message and exit
  -f {md,json}, --format {md,json}
                        Output format
  -o OUTPUT, --output OUTPUT
                        Output file; '-' = stdout
```

> **Note:** Inline JSON strings and wrapper commands (`drt`, `drb`, `drj`, `drmd`) are not supported in this version. Provide a file path as `input`.

---

## 📦 Expected input (APV-like JSON)

- Input: JSON with APV-style findings (e.g., objects including a `predicted_risk` of `low|medium|high`).  
- The summarizer normalizes case and computes:
  - `total`
  - `by_severity` (`CRITICAL|HIGH|MEDIUM|LOW|INFO` plus lowercase aliases)
  - `worst`
  - `risk_level` (`red|yellow|green`)

Example output (`-f json`):

```json
{
  "total": 3,
  "by_severity": {
    "critical": 0,
    "high": 1,
    "medium": 1,
    "low": 1,
    "info": 0,
    "CRITICAL": 0,
    "HIGH": 1,
    "MEDIUM": 1,
    "LOW": 1,
    "INFO": 0
  },
  "worst": "HIGH",
  "risk_level": "red"
}
```

---

## 🧪 Local Developer Workflow

```bash
# Dev requirements
python -m pip install --upgrade pip
pip install poetry

# Install deps
poetry install --no-interaction

# Local gates
poetry run ruff check .
poetry run black --check .
PYTHONPATH=src poetry run pytest -q
poetry run mypy src
```

---

## 🔧 CI (GitHub Actions)

- Matrix **Python 3.11 / 3.12** aligned with local gates.
- **CodeQL** and **Release Drafter** active.
- Protected `main` with required checks and squash merges.

Typical job steps:

```yaml
- run: python -m pip install --upgrade pip
- run: pip install poetry
- run: poetry install --no-interaction
- run: poetry run ruff check .
- run: poetry run black --check .
- env:
    PYTHONPATH: src
  run: poetry run pytest -q
- run: poetry run mypy src

# Example CLI use in CI
- run: poetry run python -m pip install .
- run: diff-risk examples/sample_apv.json -f md -o report.md
```

---

## 🔒 Security

- No shell customization required.
- Keep sensitive data out of public PRs.
- CodeQL is enabled.

---

## 🙌 Contributing

- Small, atomic PRs using **Conventional Commits**.
- Keep gates green before requesting review.
- Use auto-merge when checks pass.

---

## 👤 Author

**CoderDeltaLAN (Yosvel)**  
GitHub: https://github.com/CoderDeltaLAN

---

## 💚 Donations & Sponsorship

Support open-source: your donations keep projects clean, secure, and evolving for the global community.
[![Donate](https://img.shields.io/badge/Donate-PayPal-0070ba?logo=paypal&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=YVENCBNCZWVPW)

---

## 📄 License

Released under the **MIT License**. See [LICENSE](LICENSE).
