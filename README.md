# ⭐ diff-risk-dashboard — APV → Risk Summary (Python CLI)

A lean, production-grade **Python CLI** that ingests **ai-patch-verifier (APV)** JSON and outputs a clear **risk summary** as **Markdown** or **JSON**.
Designed for clean CI; use the JSON output to enforce your own merge gates in workflows.

<div align="center">

[![Manual](https://img.shields.io/badge/Manual-User%20Guide-blue?style=for-the-badge)](docs/MANUAL.md)

<br/>

[![CI / build](https://github.com/CoderDeltaLAN/diff-risk-dashboard/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/CoderDeltaLAN/diff-risk-dashboard/actions/workflows/build.yml)
[![CodeQL Analysis](https://github.com/CoderDeltaLAN/diff-risk-dashboard/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/CoderDeltaLAN/diff-risk-dashboard/actions/workflows/codeql.yml)
[![Release](https://img.shields.io/github/v/release/CoderDeltaLAN/diff-risk-dashboard?display_name=tag)](https://github.com/CoderDeltaLAN/diff-risk-dashboard/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GHCR](https://img.shields.io/badge/container-ghcr.io-blue)](../../pkgs/container/diff-risk-dashboard)
[![Donate - PayPal](https://img.shields.io/badge/Donate-PayPal-0070ba?logo=paypal&logoColor=white)](https://www.paypal.com/donate/?hosted_button_id=YVENCBNCZWVPW)

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

## 🚀 Quick Start (end users)

<!-- diff-risk:usage:start -->

### Usage (file path input)

> Input **must be a file path** to an APV JSON. Inline JSON is not supported.

```bash
# JSON output to file
diff-risk examples/sample_apv.json -f json -o out.json

# Markdown output to file
diff-risk examples/sample_apv.json -f md -o report.md

# Send to stdout
diff-risk examples/sample_apv.json -f json -o -
diff-risk examples/sample_apv.json -f md   -o -
```

<!-- diff-risk:usage:end -->

### A) Install & run locally

```bash
# 1) Clone
git clone https://github.com/CoderDeltaLAN/diff-risk-dashboard.git
cd diff-risk-dashboard

# 2) Install as package
python -m pip install --upgrade pip
python -m pip install .

# 3) Use the CLI
diff-risk examples/sample_apv.json -f md -o report.md
```

### Install & Run

#### B) From PyPI (recomendado)

```bash
python -m pip install -U pip
python -m pip install diff-risk-dashboard

# Use the CLI
diff-risk examples/sample_apv.json -f md   -o report.md
diff-risk examples/sample_apv.json -f json -o report.json
```

### CLI usage

```text
usage: diff-risk [-h] [-f {md,json}] [-o OUTPUT] input

positional arguments:
  input                 Path to ai-patch-verifier JSON file

options:
  -h, --help            Show help and exit
  -f {md,json}, --format {md,json}
                        Output format
  -o OUTPUT, --output OUTPUT
                        Output file; '-' = stdout
```

#### Example JSON output

```json
{
  "total": 3,
  "by_severity": {
    "high": 1,
    "medium": 1,
    "low": 1
  }
}
```

---

## 🧪 Local Developer Workflow (mirrors CI)

```bash
python -m pip install --upgrade pip
pip install poetry

# Dependencies
poetry install --no-interaction

# Local gates
poetry run ruff check .
poetry run black --check .
PYTHONPATH=src poetry run pytest -q
# optional:
# poetry run mypy src
```

---

## 🔧 CI (GitHub Actions)

- Matrix **Python 3.11 / 3.12** aligned with local gates.
- **CodeQL** on PRs and `main`.
- **Release Drafter** for changelog.
- Branch protection + linear history via squash.

Typical Python job steps:

```yaml
- run: python -m pip install --upgrade pip
- run: pip install poetry
- run: poetry install --no-interaction
- run: poetry run ruff check .
- run: poetry run black --check .
- env:
    PYTHONPATH: src
  run: poetry run pytest -q
# Example CLI usage in CI:
- run: poetry run python -m pip install .
- run: diff-risk examples/sample_apv.json -f md -o report.md
```

---

## 🗺 When to Use This Project

- You need a **clear, portable risk summary** from **APV** JSON.
- You want **Markdown/JSON** outputs for PRs, audits, or dashboards.

---

## 🧩 Customization

- Produce your own APV JSON and pass the file path as `input`.
- Choose output format with `--format {md,json}` and write to a file with `--output`.

---

## 🔒 Security

- No shell changes required; pure Python CLI.
- Keep sensitive APV JSON private (avoid public PRs).
- CodeQL enabled in CI.

---

## 🙌 Contributing

- Small, atomic PRs using **Conventional Commits**.
- Keep all gates green before asking for review.
- Enable auto-merge once checks pass.

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

---

<!-- sync: 2025-09-17T06:38:28Z -->
