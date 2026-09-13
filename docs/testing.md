# Testing

```bash
pip install -e ".[dev]"
pytest -q
```

Current suite:
- import smoke
- doctor hard/soft structure
- gateway bind safety

CI: `.github/workflows/python.yml` runs install, pytest, and `omega doctor`.
