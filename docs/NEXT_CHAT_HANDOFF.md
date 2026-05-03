# Next Chat Handoff

Last updated: 2026-05-03

## Start every new chat with this rule

Do not change GitHub or files immediately.

First run these verification commands and paste the output:

cd /workspaces/jee-cse-ai-placement-simulator
git fetch origin
git --no-pager status
git --no-pager log --oneline --decorate --graph -8
python -m unittest discover -s tests -v

If the working tree is not clean, stop and inspect before editing.

## Current known good state

Latest known good commit: 94b11c6 Add publication review checklist UI
Expected state: branch main is up to date with origin/main and working tree clean.
Expected tests: 30 tests pass.

## Completed in this stabilization session

1. Confirmed correct Codespace and repository.
2. Fixed corrupted frontend/review.html.
3. Added tests/test_static_frontend.py.
4. Added .github/workflows/tests.yml.
5. Verified 13/13 tests pass.
6. Verified local server pages and API endpoints.
7. Visually verified source drawer.
8. Added docs/CURRENT_STATUS_AND_RESUME_LOG.md.
9. Added docs/ISSUES_AND_BLOCKERS.md.
10. Fixed README quick-start path.
11. Marked README and source drawer blockers resolved.
12. Added dependency-free `GET /api/compare` support in `app/pure_http_server.py`.
13. Added pure HTTP endpoint tests in `tests/test_pure_http_server.py`.
14. Marked BLK-006 resolved in `docs/ISSUES_AND_BLOCKERS.md`.
15. Centralized industry-standard Maharashtra-only versioning in `app/version.py`.
16. Removed beta wording from active docs.
17. Added `/api/readiness` launch gate for Maharashtra v1.0 readiness.
18. Added readiness tests in `tests/test_readiness.py`.
19. Added global v1.0 publication checks in `data/publication_checks.csv`.
20. Added per-program publication review rows in `data/program_publication_reviews.csv`.
21. Added `/api/publication-review/{program_key}` endpoint.
22. Added endpoint tests in `tests/test_publication_review_endpoint.py`.
23. Wired `frontend/review.html` and `frontend/review.js` to consume `/api/publication-review/{program_key}`.
24. Added static frontend coverage that verifies the review page uses the publication-review API.
25. Verified 30/30 tests pass after the review UI change.
26. Committed and pushed `94b11c6 Add publication review checklist UI`.

## Current app state

This is still a Maharashtra-only local pilot, not the final production simulator.
Data status: 15 total rows, 1 default visible row, 14 hidden pending verification rows, 26 source rows.
Do not promote hidden rows to publish_default=yes unless source, cutoff, denominator, fee, confidence, and last-verified checks pass.

## Verified local commands

Run tests: python -m unittest discover -s tests -v
Run server: python -m app.pure_http_server
The server terminal staying busy is normal. Stop it with Ctrl+C.

## Remaining important blockers

Open blockers are tracked in docs/ISSUES_AND_BLOCKERS.md.
Most important next blockers: BLK-001 to BLK-004. `/api/readiness` now exposes the Maharashtra v1.0 launch blockers. Next work should reduce those blockers through row-level verification, stronger source/value provenance, readiness blockers, and scoring hardening. The review UI now shows publication checks but remains read-only and local-note-only.

## Recommended next controlled part

Part 8: push toward Maharashtra v1.0 readiness with strict source gates and no public overclaiming.
Do not start by editing. First inspect files, confirm clean repo, run tests, then decide.

## Recommended next chat opening prompt

Continue the JEE/CAP CSE-AI Job & Placement Simulator from docs/NEXT_CHAT_HANDOFF.md. Use Codespaces only for execution. First run startup verification commands. Do not change files until repo is clean and 30 tests pass. Current product direction is Maharashtra v1.0 readiness. Latest known good commit should be 94b11c6 Add publication review checklist UI. Next likely task is to inspect /api/readiness and docs/ISSUES_AND_BLOCKERS.md, then choose the smallest safe source-gated step for BLK-001 to BLK-004. Do not promote hidden rows.


## Execution rule after 2026-05-03 break

Use Codespaces as the execution environment. ChatGPT should guide with copy-paste commands, and the user should paste terminal outputs. Do not rely on GitHub connector edits for this project unless explicitly requested. Before any edit, run startup verification commands and confirm clean working tree plus expected tests passing.

Current known-good checkpoint before break:
- Commit: 94b11c6 Add publication review checklist UI
- Tests: 30 passing
- Scope: Maharashtra only
- Product direction: Maharashtra v1.0 readiness
- Data safety: do not promote hidden rows or set publish_default=yes until required publication checks pass.
