# Diff Risk Dashboard — User Manual

> **Version:** v0.4.x • **Scope:** Complete guide for end‑users and maintainers  
> **Project:** `diff-risk-dashboard` — APV → Risk Summary (Python CLI)

---

## Table of Contents
- [1. What is this?](#1-what-is-this)
- [2. Who is it for](#2-who-is-it-for)
- [3. Installation](#3-installation)
- [4. Quick Start](#4-quick-start)
- [5. Inputs (APV JSON)](#5-inputs-apv-json)
- [6. Output formats](#6-output-formats)
- [7. Exit codes & CI gating](#7-exit-codes--ci-gating)
- [8. Short wrappers](#8-short-wrappers)
- [9. CLI reference](#9-cli-reference)
- [10. CI/CD integration (GitHub Actions)](#10-cicd-integration-github-actions)
- [11. Color/TTY tips](#11-colortty-tips)
- [12. Troubleshooting](#12-troubleshooting)
- [13. FAQ](#13-faq)
- [14. Security & Privacy](#14-security--privacy)
- [15. Contributing](#15-contributing)
- [16. Versioning & Releases](#16-versioning--releases)
- [17. Support](#17-support)
- [18. License](#18-license)

---

## 1. What is this?
`diff-risk-dashboard` is a lean, production‑grade **Python CLI** that ingests
**ai‑patch‑verifier (APV)** JSON and emits a **risk summary** in **table**, **JSON**,
or **Markdown**. It is designed for **always‑green CI**, providing clear **exit codes**
to gate merges by risk level.

### Key capabilities
- Normalize APV severities (`CRITICAL|HIGH|MEDIUM|LOW|INFO`, case‑insensitive).
- Summaries: `total`, `by_severity`, `worst`, and aggregate `risk_level`.
- Output suitable for **terminals**, **bots**, **PR comments**, and **dashboards**.

---

## 2. Who is it for
- **Developers & DevOps**: need deterministic summaries to automate merge gates.
- **Security/QA**: require exportable JSON/Markdown for audits and reporting.
- **Team leads**: want a quick “is it safe to merge?” signal in CI.

---

## 3. Installation

### Option A — pipx (recommended)
```bash
pipx install .    # run in project root, or: pipx install git+https://github.com/CoderDeltaLAN/diff-risk-dashboard.git
```

### Option B — pip (user site)
```bash
python -m pip install --user .
```

### Option C — development (Poetry)
```bash
pip install poetry
poetry install --no-interaction
```

> After installing, the `diff-risk` command is available on your PATH.

---

## 4. Quick Start

Run with the bundled sample:
```bash
diff-risk examples/sample_apv.json -f table
```

Generate Markdown to a file:
```bash
diff-risk examples/sample_apv.json -f md -o report.md
```

Inline JSON (single quotes outside, double inside):
```bash
diff-risk '{"by_severity":{"CRITICAL":0,"HIGH":1,"MEDIUM":1,"LOW":1,"INFO":0}}' -f table
```

---

## 5. Inputs (APV JSON)

The tool accepts either:
1) **File path** to JSON, or
2) **Inline JSON** text (starting with `{` or `[`).

Minimum shapes supported:
- **Aggregated**:
  ```json
  { "by_severity": { "HIGH": 1, "MEDIUM": 2, "LOW": 3 } }
  ```
- **Flat list** (each item has a severity/level field):
  ```json
  [
    {"severity":"high", "title":"..."},
    {"predicted_risk":"medium", "id": 42}
  ]
  ```

The CLI normalizes severities and computes:
- `total`
- `by_severity` (both UPPER and lower keys are included for convenience)
- `worst` (string)
- `risk_level`: `"red" | "yellow" | "green"`

---

## 6. Output formats

### Table (TTY‑friendly)
```bash
diff-risk input.json -f table
```

### JSON (machines/CI)
```bash
diff-risk input.json -f json
```

Example JSON:
```json
{
  "total": 3,
  "by_severity": {
    "CRITICAL": 0, "HIGH": 1, "MEDIUM": 1, "LOW": 1, "INFO": 0,
    "critical": 0, "high": 1, "medium": 1, "low": 1, "info": 0
  },
  "worst": "HIGH",
  "risk_level": "red"
}
```

### Markdown (reports/PRs)
```bash
diff-risk input.json -f md -o _intel/report.md
```

---

## 7. Exit codes & CI gating

Default behavior (raw CLI):
- `green` → exit **0**
- `yellow` → exit **1**
- `red` → exit **2**

To force **always 0** (useful locally or for non‑blocking jobs):
```bash
diff-risk input.json --no-exit-by-risk
```

---

## 8. Short wrappers

Convenience scripts (installed in `bin/`):
- `drt <apv.json | raw-json>` — colored table (TTY)
- `drb <apv.json | raw-json>` — bars (logs)
- `drj <apv.json | raw-json>` — JSON (CI)
- `drmd <apv.json | raw-json>` — Markdown (stdout)

Examples:
```bash
drt examples/sample_apv.json
drt '{"by_severity":{"CRITICAL":0,"HIGH":1,"MEDIUM":1,"LOW":1,"INFO":0}}'
APV="/absolute/path/to/your_apv.json"; drt "$APV"
```

Add to PATH:
```bash
mkdir -p ~/.local/bin && ln -sf "$PWD/bin/"* ~/.local/bin/ && hash -r
```

---

## 9. CLI reference

```bash
diff-risk -h
```

Options (common):
- `-f, --format {table,json,md,bar}` — output format
- `-o, --output` — file path; `-` = stdout
- `--no-exit-by-risk` — disable exit code gating

---

## 10. CI/CD integration (GitHub Actions)

Minimal job (Python 3.11 / 3.12):
```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
- run: python -m pip install --upgrade pip
- run: pip install poetry
- run: poetry install --no-interaction
- run: poetry run ruff check .
- run: poetry run black --check .
- env:
    PYTHONPATH: src
  run: poetry run pytest -q
- run: poetry run mypy src
# Smoke:
- run: |
    poetry build
    poetry run python -m pip install .
    diff-risk examples/sample_apv.json -f md -o _intel/report.md
```

Upload report artifact:
```yaml
- uses: actions/upload-artifact@v4
  with:
    name: sample-report
    path: _intel/report.md
```

---

## 11. Color/TTY tips

To force colorized output in recordings/CI logs:
```bash
script -qfc "drt examples/sample_apv.json" /dev/null
```

---

## 12. Troubleshooting

- **JSONDecodeError**: Your argument is neither a readable file nor valid JSON.  
  Use a valid path or wrap inline JSON like: `'{"by_severity":{"HIGH":1}}'`.

- **Exit code > 0 unexpectedly**: You likely used the raw CLI without
  `--no-exit-by-risk`. The wrappers already add it for you.

- **Command not found**: Ensure the package is installed and/or PATH updated
  when using wrappers.

---

## 13. FAQ

**Q:** Can I feed arbitrary JSON?  
**A:** Provide either the aggregated `by_severity` or a list with `severity`/`predicted_risk` keys.

**Q:** Why duplicate lower & upper keys in `by_severity`?  
**A:** Convenience for consumers with strict schemas.

---

## 14. Security & Privacy

- No credentials required. Do **not** upload sensitive JSON to public PRs.
- CodeQL runs in CI; keep dependencies updated.

---

## 15. Contributing

- Follow **Conventional Commits**.
- Keep **ruff/black/pytest/mypy** green before requesting review.
- Prefer small PRs with auto‑merge enabled after checks.

---

## 16. Versioning & Releases

- Tags `vMAJOR.MINOR.PATCH`. Release notes are drafted automatically.
- Use GitHub Releases to fetch artifacts and changelog.

---

## 17. Support

- Open Issues or Discussions on GitHub.
- For commercial support, contact the repository owner.

---

## 18. License

Released under the **MIT License**. See [LICENSE](../LICENSE).

---

> **Tip:** The README “Manual” badge links to this page.
