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

Latest known good commit: 3472b50 Docs: add next chat handoff
Expected state: branch main is up to date with origin/main and working tree clean.
Expected tests: 13 tests pass.

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
Most important next blocker: BLK-006. app/pure_http_server.py imports compare, but does not expose /api/compare.
FastAPI has POST /compare in app/api_app.py, and compare() exists in app/simulator_core.py.

## Recommended next controlled part

Part 6: inspect and add or document /api/compare support in app/pure_http_server.py.
Do not start by editing. First inspect files, confirm clean repo, run tests, then decide.

## Recommended next chat opening prompt

Continue the JEE/CAP CSE-AI Job & Placement Simulator from docs/NEXT_CHAT_HANDOFF.md. First help me run startup verification commands. Do not change files until repo is clean and tests pass. Next likely task is BLK-006: inspect/add /api/compare support in app/pure_http_server.py, with tests, then update docs/ISSUES_AND_BLOCKERS.md.
