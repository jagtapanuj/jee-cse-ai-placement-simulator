# Issues and Blockers Register

Last updated: 2026-05-03

This file records known issues, partial implementations, and blockers for the JEE/CAP CSE-AI Job & Placement Simulator local pilot.

The current app is a Maharashtra-only local pilot. It is not ready for public launch.

## Severity levels

| Severity | Meaning |
|---|---|
| P0 | Blocks trust, safety, testing, or public readiness. |
| P1 | Important before internal beta or next serious build stage. |
| P2 | Cleanup, polish, or later hardening. |

## Current open issues and blockers

| ID | Severity | Area | Issue | Current status | Next action |
|---|---:|---|---|---|---|
| BLK-001 | P0 | Data safety | 14 out of 15 program rows are hidden pending verification. | Open | Keep hidden rows as `publish_default=no` until source, cutoff, denominator, fee, confidence, and last-verified checks pass. |
| BLK-002 | P0 | Data model | Current CSV model is useful for pilot but does not yet implement full value-level provenance for every visible number. | Open | Design proper source/value/staging schema before public launch. |
| BLK-003 | P0 | Admin workflow | Review checklist saves only in browser localStorage. It does not update dataset, GitHub, database, or audit logs. | Open | Treat review page as temporary helper only. Build real verification workflow later. |
| BLK-004 | P0 | Public launch | Product is not public-ready. | Open | Do not launch until source-linked values, validation gates, admin workflow, and stronger QA pass. |
| BLK-005 | P1 | README/docs | README/run instructions mentioned an old nested folder path such as `Maharashtra_Simulator_LocalApp_v7`. | Resolved | README quick-start now points to the repository root. |
| BLK-006 | P1 | API consistency | `pure_http_server.py` did not expose `/api/compare`, even though compare logic existed in core/FastAPI path. | Resolved | Added dependency-free `GET /api/compare` support with publish-default safety gate tests. |
| BLK-007 | P1 | Version naming | API reported an old patch-era data version string in multiple places. | Resolved | Centralized app/data version naming in `app/version.py` and updated health/data payloads. |
| BLK-008 | P1 | Source drawer | Source drawer API and visual drawer interaction were manually checked in browser. | Resolved | Source drawer opens, displays evidence/source/audit sections, and closes correctly in local pilot. |
| BLK-009 | P1 | Scoring | Current job scores appear stored in CSV fields rather than computed fully from raw denominator-aware verified evidence. | Open | Build formula-backed scoring after schema/provenance work. |
| BLK-010 | P1 | Admission engine | Current admission bucket logic is basic and not yet a full JoSAA/CSAB/CAP/JAC/private route engine. | Open | Expand route-specific engine only after stabilization. |
| BLK-011 | P1 | Placement evidence | Placement evidence is not yet full denominator-aware production model. | Open | Add total/eligible/opted/placed/higher-studies/off-campus fields in future schema. |
| BLK-012 | P1 | Testing | Static frontend tests now exist, but there are still no browser/E2E tests. | Open | Add lightweight endpoint/UI tests later if project grows. |
| BLK-013 | P2 | Backup branch | Temporary backup branch `backup-before-rebase-manual-fix` exists locally. | Open | Keep for now; delete only after several clean commits if no longer needed. |
| BLK-014 | P2 | UI polish | UI is functional but still a local pilot, not production UX. | Open | Do not polish heavily until data model and admin workflow are stronger. |

## Recently resolved issues

| ID | Area | Resolution |
|---|---|---|
| RES-001 | Frontend corruption | `frontend/review.html` corrupted markup was repaired. |
| RES-002 | Static frontend QA | Added `tests/test_static_frontend.py` to catch repeated HTML shell/corruption problems. |
| RES-003 | CI testing | Added `.github/workflows/tests.yml` to run unit tests on GitHub push/pull request. |
| RES-004 | Local verification | Home, queue, review pages and main API endpoints returned `200 OK` in manual local test. |
| RES-005 | README/docs | README quick-start was corrected to run from the repository root instead of the old nested folder path. |
| RES-006 | Source drawer | Source drawer was visually verified in browser: opens, shows evidence/source/audit sections, and closes correctly. |
| RES-007 | API consistency | Added `/api/compare` to the dependency-free pure HTTP server and covered it with endpoint tests. |
| RES-008 | Version naming | Centralized app/data version naming with `app/version.py` and removed old patch-era API version strings. |

## Safety rules

- Do not promote hidden rows to `publish_default=yes` during cleanup.
- Do not change college data values without source verification.
- Do not claim guaranteed admission, job, branch, salary, or package.
- Do not treat internal testing mode as public output.
- Do not polish public UI before data model, source registry, admin verification workflow, and scoring tests are stronger.
- Every future code/data change should be done in small approved parts.

## Recommended next parts

1. Visually test the source drawer button.
2. Inspect and fix README run instructions if outdated.
3. Inspect `/api/compare` support in the dependency-free server.
4. Push toward Maharashtra v1.0 readiness: source-gated data, schema/provenance, admin workflow, and scoring hardening.
5. Plan the next real architecture step: proper schema/provenance/admin workflow.
