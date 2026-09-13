# Development

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # add keys only if calling live providers
```

## Run
```bash
python bin/omega doctor
python bin/omega gateway start
python bin/omega ide
# or foreground: python bin/omega-gateway
```

## Test
```bash
pytest -q
```

## Conventions
- Stdlib-first; new deps need PR justification
- Loopback gateway by default
- No secrets in repo
- Small commits; keep public API compatible
