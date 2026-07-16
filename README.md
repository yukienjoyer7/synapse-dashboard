# SYNAPSE HealthOps

SYNAPSE HealthOps is a Streamlit decision-support dashboard for reviewing digital
readiness, investment conversion, operational pressure, and intervention priorities
across 276 Indonesian hospitals.

## Development

```bash
uv sync --frozen --group dev
uv run streamlit run dashboard/app.py
```

Quality checks:

```bash
uv run --group dev ruff check .
uv run --group dev ruff format --check .
uv run --group dev pytest -q
```

The application consumes precomputed hospital-level CSV and JSON artifacts. It does
not train or load machine-learning models at runtime.

