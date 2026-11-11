# Assignment 07: Reproducible Data Pipelines

Install the locked environment and reproduce all derived datasets:

```bash
uv sync
uv run dvc repro
```

The original input is `data/raw/events.csv` (2,000 rows). It is a pipeline
dependency, not a standalone DVC-tracked output. No DVC remote is required.

- `scripts/clean.py` removes missing fields, invalid event types, and non-positive
  durations; writes integer seconds and timestamps in `YYYY-MM-DDTHH:MM:SS` format.
  Valid event types are `click`, `login`, `purchase`, `scroll`, and `view`.
  Nonintegral durations are rejected rather than truncated; malformed timestamps
  fail explicitly. The original dataset yields 1,612 clean rows.
- `scripts/transform.py` adds `date` in `YYYY-MM-DD` format.
- `scripts/features.py` adds `duration_minutes` and full English `weekday` names.

Each stage creates its output directory. DVC tracks scripts, input CSVs, and the
package manifests as dependencies, with derived CSVs as outputs. `dvc.lock`
records their hashes; all derived outputs can be rebuilt from the raw input even
without a DVC cache. The raw CSV must remain available locally.

The final columns are `user_id`, `timestamp`, `event_type`, `duration_seconds`,
`date`, `duration_minutes`, and `weekday`.

Run data validation and open the duration histogram notebook:

```bash
uv run python tests/verify_pipeline.py
uv run marimo check notebooks/report.py
uv run marimo edit notebooks/report.py
```
