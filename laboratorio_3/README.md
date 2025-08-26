# Laboratorio 3 — Codespaces, venv, ruff, mypy, pytest

## Reproducir
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ruff check . && ruff format .
mypy .
pytest -q
