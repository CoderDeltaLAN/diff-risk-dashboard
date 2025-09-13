# Diff Risk Dashboard

Summarizes AI Patch Verifier (APV) JSON into a clean, professional terminal table, text bars, JSON, or Markdown report.

<!-- diff-risk:usage:start -->

## 🚀 Usage

### Short commands
- `drt <apv.json | raw-json>` — color table (TTY)
- `drb <apv.json | raw-json>` — text bars (logs)
- `drj <apv.json | raw-json>` — JSON (CI)
- `drmd <apv.json | raw-json>` — Markdown (stdout)

```bash
# Demo (bundled sample)
drt examples/sample_apv.json

# Inline JSON (single quotes outside, double quotes inside)
drt '{"by_severity":{"CRITICAL":0,"HIGH":1,"MEDIUM":1,"LOW":1,"INFO":0}}'

# Your real file
APV="/absolute/path/to/your_apv.json"; drt "$APV"

# Other formats with the same input
drb "$APV"              # bars (logs)
drj "$APV"              # JSON (CI)
mkdir -p _intel && drmd "$APV" > _intel/report.md  # Markdown to file

# Force colors for recordings
script -qfc "drt $APV" /dev/null
```

> Exit codes: `0=green`, `1=yellow`, `2=red`. Use `--no-exit-by-risk` to force `0` in demos.

<!-- diff-risk:usage:end -->
