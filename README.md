# Maharashtra CSE/AI Job & Placement Simulator — Local App v7

This is the first Codex/GitHub-ready local implementation of the Maharashtra-only JEE/CAP CSE-AI job and placement simulator.

It converts the v6 verified/staged dataset into a small runnable app with:

- strict `publish_default` safety gate
- local simulator core
- optional FastAPI wrapper
- dependency-free HTTP server + minimal UI
- source drawer endpoint
- compare endpoint
- regression tests
- data-quality tests
- PostgreSQL starter schema/seed files

## Non-negotiable data rule

No cutoff, placement, salary, fee, or seat value should be shown publicly unless it has source, year, branch/program, denominator where relevant, confidence, and last-verified status.

By default, the API returns only rows with `publish_default = yes`. Use `include_partial=true` only for internal testing.

## Quick start without dependencies

```bash
python -m app.pure_http_server
```

Open:

```text
http://127.0.0.1:8000
```

API examples:

```text
http://127.0.0.1:8000/api/health
http://127.0.0.1:8000/api/programs
http://127.0.0.1:8000/api/simulate?rank=300&rank_type=MHT_CET_MERIT
http://127.0.0.1:8000/api/simulate?rank=300&rank_type=MHT_CET_MERIT&include_partial=true
```

## Optional FastAPI mode

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.api_app:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

Current expected status:

- total rows loaded: 15
- default visible rows: 1
- hidden pending verification: 14

This is intentionally conservative.

## What is not done yet

- This is not a public launch.
- CAP/JoSAA row-level extraction still needs deeper verification for more colleges.
- Admin verification workflow is not fully built yet.
- More rows must pass source/denominator/fee/cutoff verification before default visibility increases.
