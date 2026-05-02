# Codex Handoff Instructions

You are working on the Maharashtra CSE/AI Job & Placement Simulator.

## Goal

Turn the local pilot into a trustworthy app. Do not convert hidden rows into public rows unless their data quality gate passes.

## Important rules

1. Do not claim guaranteed admission, job, branch, or package.
2. Do not show unverified rows by default.
3. Preserve `publish_default` behavior.
4. Keep source drawer visible for every result.
5. Add tests before changing scoring/gating logic.
6. Keep MHT-CET, JoSAA, CSAB, and private routes separated.
7. Do not compare JEE Main AIR directly with MHT-CET merit rows unless the source row is an AI/JEE seat and verified.

## First coding tasks

1. Run `python -m unittest discover -s tests -v`.
2. Start `python -m app.pure_http_server` and test the local UI.
3. Add a proper `/api/data-quality` endpoint.
4. Add a full source drawer UI panel in the frontend.
5. Build a small admin-only page that lists hidden rows and their blockers.
6. Do not modify `data/programs.csv` values unless the matching source evidence is verified.
