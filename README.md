# SYNAPSE HealthOps

SYNAPSE HealthOps is a Streamlit decision-support dashboard for reviewing digital
readiness, investment conversion, operational pressure, and intervention priorities
across a cross-sectional sample of 276 Indonesian hospitals.

The public repository is available at
[github.com/yukienjoyer7/synapse-dashboard](https://github.com/yukienjoyer7/synapse-dashboard).

## Decision workflow

The six pages move from portfolio signals to hospital-level evidence:

1. **Ringkasan eksekutif** — portfolio condition, geographic concentration, and watchlist.
2. **Kesiapan digital & investasi** — maturity, adoption, resources, and conversion gaps.
3. **Dampak terhadap operasional** — persisted adjusted associations and burden profiles.
4. **Prioritas intervensi** — governed scoring, bottlenecks, owners, and action cohorts.
5. **Eksplorasi rumah sakit** — fixed class-peer comparison and score decomposition.
6. **Metodologi & kualitas data** — formulas, model gates, missingness, and limitations.

Global filters persist between pages. Hospital selections made from charts and tables
also carry into the explorer. Empty filters mean the full portfolio.

## Architecture

```text
Analytics notebook
  -> immutable CSV/JSON artifacts
  -> validated and cached pandas loader
  -> lightweight filtering and aggregation
  -> Streamlit pages, Plotly charts, native tables, and CSV exports
```

The dashboard is intentionally a presentation and decision-support layer. It does not:

- train or load machine-learning models at runtime;
- run regression, scenario simulation, or individual prediction at runtime;
- require a database, API, authentication service, or external data connection;
- reinterpret an association as a causal effect.

Model coefficients, confidence intervals, out-of-fold estimates, peer statistics,
scores, tiers, and recommendations are loaded from notebook-produced artifacts.

## Local development

Requirements:

- Python 3.11 or newer;
- [uv](https://docs.astral.sh/uv/).

Install the locked environment and start the app:

```bash
uv sync --frozen --group dev
uv run --group dev streamlit run streamlit_app.py
```

Streamlit opens at `http://localhost:8501` by default. No secrets or environment
variables are required.

Run the complete quality gate:

```bash
uv run --group dev ruff check .
uv run --group dev ruff format --check .
uv run --group dev pytest -q
```

The tests cover the artifact contract, governed portfolio counts, filters, formatting,
peer medians, export metadata, chart builders, and all Streamlit entry points.

## Repository structure

```text
dashboard/
  application.py          Multipage shell, navigation, and global sidebar
  app.py                  Backward-compatible legacy launcher
  app_pages/              Six decision-oriented pages
  components/             Reusable charts, cards, tables, and visual theme
  styles/                 Scoped design-system CSS
  utils/                  Formatting and metadata-aware CSV export
  data_loader.py          Cached artifact loading and contract validation
synapse_artifacts/        Versioned runtime CSV and JSON artifacts
docs/                     Product context, design system, structure, and stack specs
tests/                    Unit, contract, chart, and Streamlit smoke tests
.streamlit/config.toml    HealthOps theme and browser configuration
streamlit_app.py          Canonical local and Community Cloud entry point
pyproject.toml            Runtime and development dependencies
uv.lock                   Reproducible dependency lock
```

## Data contract and provenance

`hospital_features_scored.csv` is the primary runtime dataset. The loader requires
exactly 276 unique hospital IDs and verifies full ID coverage in the priority, peer,
and root-cause artifacts. It also checks required columns and ensures priority weights
sum to 1.0.

Runtime artifacts include:

- scored hospital features, priority tiers, peer benchmarks, and root-cause scores;
- intervention recommendations and executive findings;
- descriptive and HC3-adjusted association outputs;
- model summaries, validation gates, analysis configuration, and data-quality audit.

The displayed data version is generated from the SHA-256 digest of the primary scored
artifact, for example `data-21708194a0d4`. Every CSV download repeats four provenance
fields on every row: UTC export timestamp, active filters, benchmark definition, and
data version. Files use UTF-8 with a BOM for spreadsheet compatibility.

### Benchmark behavior

Hospital peer benchmarks always use the complete cohort with the same hospital class.
They do not shrink when a dashboard filter is applied. Filtered KPI cards may compare
with the full portfolio, while the page subtitle and export metadata state which
benchmark is in use.

### Refreshing analytics artifacts

1. Re-run the upstream analytical notebook.
2. Replace the corresponding files in `synapse_artifacts/` without changing their names.
3. Run the full quality gate.
4. Review any changed governed counts, thresholds, coefficients, and model gates.
5. Commit the artifact update separately from UI or application changes.

If a required file, column, ID, or configuration value is invalid, the app fails with
an explicit contract error instead of generating fallback data.

## Deployment

The repository is ready for Streamlit Community Cloud:

1. Select this GitHub repository and the `main` branch.
2. Set the main file path to `streamlit_app.py`.
3. Deploy without secrets; all runtime artifacts are versioned in the repository.

`uv.lock` and `pyproject.toml` define the environment. The app is repository-ready but
is not automatically deployed by this project setup.

## Analytical limitations

- The dataset is observational and cross-sectional, so findings are not causal.
- The 276-hospital sample is not claimed to be a national estimate or census.
- BOR thresholds are analytical configuration, not a universal quality standard.
- LOS needs case-mix context; binary adoption does not measure implementation quality.
- Expected maturity is a model estimate, not an official target or counterfactual.
- The operational predictive model failed its validation gate, so the app does not
  expose individual forecasts, simulations, or feature attribution.
- Priority scores order assessment work; they are not clinical risk probabilities.

## Version-control conventions

Development uses small conventional commits such as `feat(data):`, `feat(ui):`,
`feat(operations):`, `test:`, and `docs:`. This keeps data, infrastructure, page,
quality, and documentation changes independently traceable.
