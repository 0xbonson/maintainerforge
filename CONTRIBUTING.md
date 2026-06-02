# Contributing

Thanks for helping improve TriageForge.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
ruff check .
```

## Pull requests

Keep changes focused. Include tests for behavior changes. For security-sensitive changes, explain the risk and why the implementation is safe.
