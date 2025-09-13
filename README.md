# diff-risk-dashboard

Visual dashboard for Pull Request risk exposure, designed to consume **ai-patch-verifier** JSON outputs.

## Quick Start
```bash
poetry install
poetry run drd summarize examples/sample_apv.json
```

## Run checks (mirrors CI)
```bash
poetry run ruff check .
poetry run black --check .
PYTHONPATH=src poetry run pytest -q
poetry run mypy src
```

## License
MIT
