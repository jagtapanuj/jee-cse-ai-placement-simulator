# Current Status and Resume Log

Last updated: 2026-05-03

## Repository

- Repository: `jagtapanuj/jee-cse-ai-placement-simulator`
- Default branch: `main`
- Current latest known commit before this documentation update: `0e537540f9e607519d804f6091920a1dd004b0c5`
- Latest known commit title before this documentation update: `Patch v10: add row review checklist`
- Current implementation type: Maharashtra-only local pilot app, not the full final production simulator.

## Current product stage

The project is currently in a local pilot / internal alpha state.

The implemented app is a small, source-gated Maharashtra-focused simulator with:

- dependency-free local HTTP server
- optional FastAPI wrapper
- CSV-based program/source/audit data
- conservative `publish_default` gate
- minimal frontend UI
- data-quality summary endpoint
- readable source drawer
- verification queue page
- local browser-only review checklist page
- basic unit/data-quality tests

It is not ready for public launch.

## Current data state

Current known data status from the repo:

- Total program rows: 15
- Default visible rows: 1
- Hidden pending verification rows: 14
- Default-visible pilot row: `PROG-V5-004` / SPIT Mumbai / CSE-AIML
- Most rows remain hidden due to missing verified cutoff rows, staged admission verification, missing denominator/median/fee checks, provisional placement status, or placement not being score-ready.

Important rule: hidden rows must not be promoted to default/public visibility until source, cutoff, denominator, fee, confidence, and last-verified checks pass.

## Current implemented files and purpose

### Backend / core

- `app/models.py` — CSV row model and parsing helpers.
- `app/data_loader.py` — loads `programs.csv`, `source_register.csv`, and `data_quality_audit.csv`.
- `app/simulator_core.py` — admission bucket logic, visibility gate, simulation output, data-quality summary, source drawer, compare logic.
- `app/pure_http_server.py` — dependency-free local HTTP server and frontend/static file serving.
- `app/api_app.py` — optional FastAPI API wrapper.

### Data

- `data/programs.csv` — current staged/pilot program rows and score fields.
- `data/source_register.csv` — indexed source links and source status.
- `data/data_quality_audit.csv` — row-level readiness/blocker notes.

### Frontend

- `frontend/index.html` — local simulator landing/input/result UI.
- `frontend/app.js` — simulator UI logic and source drawer rendering.
- `frontend/queue.html` — internal verification queue page.
- `frontend/queue.js` — queue filtering and blocker grouping.
- `frontend/review.html` — intended one-row review checklist page; currently known to contain corrupted markup.
- `frontend/review.js` — localStorage-only review checklist logic.
- `frontend/styles.css` — frontend styling.

### Tests

- `tests/test_core.py` — tests conservative gate, source drawer, bucket logic, compare gate, data-quality summary.
- `tests/test_data_quality.py` — tests basic program/source data quality rules.

### Docs

- `README.md` — quick start and current expected data status.
- `docs/NEXT_STEPS.md` — older next-step note from v8 patch.
- `docs/IMPLEMENTATION_STATUS_v8_PATCH.md` — v8 patch description.

## Known current problems

1. `frontend/review.html` is corrupted and must be fixed before relying on the review page.
2. README quick-start path may be misleading because it says `cd Maharashtra_Simulator_LocalApp_v7`, while current fetched repo files are at the repository root.
3. `pure_http_server.py` imports `compare` but does not appear to expose a `/api/compare` route.
4. Review checklist saves only to browser `localStorage`; it is not a real admin/database/GitHub-backed verification workflow.
5. Current CSV model does not yet implement full atomic value provenance required by the master blueprint.
6. Current scoring appears stored in CSV fields, not fully computed from verified denominator-aware raw data.
7. Frontend static files do not yet have tests to catch corrupted HTML.
8. The project has no complete production admin publish/rollback workflow yet.
9. No public beta/launch should happen in the current state.

## What is safe to do next

The next safest work sequence is:

1. Add or update issue/blocker documentation.
2. Add frontend/static tests that catch obvious HTML corruption.
3. Fix `frontend/review.html` only after the corruption is documented and tests exist.
4. Update README path/run instructions after verifying actual repo structure.
5. Run or ask user to run tests locally.
6. Only then continue with admin workflow/data verification improvements.

## What must not be done yet

- Do not promote hidden rows to `publish_default=yes`.
- Do not change college data values without source verification.
- Do not publish as a public product.
- Do not add more UI polish before stabilizing the current app.
- Do not merge MHT-CET and JEE rank logic.
- Do not claim guaranteed admission, job, branch, salary, or package.

## Resume prompt for next session

Continue from `docs/CURRENT_STATUS_AND_RESUME_LOG.md`. Do not change GitHub files without permission. First inspect `docs/ISSUES_AND_BLOCKERS.md`, then decide whether to add tests for corrupted static frontend files or fix `frontend/review.html` after approval.
