from __future__ import annotations

from typing import Any, Dict, List

from .data_loader import load_programs, load_publication_checks, load_quality_audit, load_sources
from .version import APP_VERSION, DATA_SCOPE, TARGET_PRODUCTION_VERSION


MIN_DEFAULT_VISIBLE_ROWS_FOR_V1 = 30
REQUIRED_PUBLIC_STATUS = "PILOT_SCORE_READY_VERIFIED"


def _program_blockers() -> List[Dict[str, Any]]:
    blockers = []
    for program in load_programs():
        row_blockers = []

        if not program.program_key:
            row_blockers.append("missing_program_key")
        if not program.college:
            row_blockers.append("missing_college")
        if not program.program:
            row_blockers.append("missing_program")
        if not program.route:
            row_blockers.append("missing_route")
        if not program.source_url_list():
            row_blockers.append("missing_source_url")
        if program.publish_default and program.data_quality_status != REQUIRED_PUBLIC_STATUS:
            row_blockers.append("published_without_required_quality_status")
        if program.publish_default and program.internal_job_score_v3 is None:
            row_blockers.append("published_without_job_score")
        if not program.publish_default:
            row_blockers.append("hidden_pending_verification")

        if row_blockers:
            blockers.append({
                "program_key": program.program_key,
                "college": program.college,
                "program": program.program,
                "publish_default": program.publish_default,
                "data_quality_status": program.data_quality_status,
                "why_not_ready": program.why_not_ready,
                "blockers": row_blockers,
            })

    return blockers


def readiness_report() -> Dict[str, Any]:
    programs = load_programs()
    sources = load_sources()
    audit_rows = load_quality_audit()
    publication_checks = load_publication_checks()

    default_visible = [p for p in programs if p.publish_default]
    hidden = [p for p in programs if not p.publish_default]
    public_rows_with_sources = [p for p in default_visible if p.source_url_list()]
    public_rows_verified = [
        p for p in default_visible
        if p.data_quality_status == REQUIRED_PUBLIC_STATUS and p.internal_job_score_v3 is not None
    ]

    blockers = _program_blockers()

    launch_blockers = []
    if len(default_visible) < MIN_DEFAULT_VISIBLE_ROWS_FOR_V1:
        launch_blockers.append({
            "id": "launch_minimum_visible_rows",
            "severity": "P0",
            "message": f"Maharashtra v1.0 requires at least {MIN_DEFAULT_VISIBLE_ROWS_FOR_V1} default-visible verified rows. Current default-visible rows: {len(default_visible)}.",
        })

    if hidden:
        launch_blockers.append({
            "id": "hidden_rows_pending_verification",
            "severity": "P0",
            "message": f"{len(hidden)} rows are still hidden pending verification. Keep them hidden until source, cutoff, denominator, fee, confidence, and last-verified checks pass.",
        })

    if len(public_rows_with_sources) != len(default_visible):
        launch_blockers.append({
            "id": "public_rows_missing_sources",
            "severity": "P0",
            "message": "Every default-visible row must have source URLs.",
        })

    if len(public_rows_verified) != len(default_visible):
        launch_blockers.append({
            "id": "public_rows_not_verified",
            "severity": "P0",
            "message": f"Every default-visible row must have status {REQUIRED_PUBLIC_STATUS} and a job score.",
        })

    public_launch_ready = not launch_blockers

    return {
        "app_version": APP_VERSION,
        "target_production_version": TARGET_PRODUCTION_VERSION,
        "data_scope": DATA_SCOPE,
        "public_launch_ready": public_launch_ready,
        "current_stage": "staging" if not public_launch_ready else "production_ready",
        "summary": {
            "total_program_rows": len(programs),
            "default_visible_rows": len(default_visible),
            "hidden_pending_verification_rows": len(hidden),
            "source_register_rows": len(sources),
            "quality_audit_rows": len(audit_rows),
            "publication_check_rows": len(publication_checks),
            "required_publication_checks": len([c for c in publication_checks if str(c.get("required_for_v1", "")).lower() == "yes"]),
            "minimum_default_visible_rows_for_v1": MIN_DEFAULT_VISIBLE_ROWS_FOR_V1,
            "default_visible_rows_with_sources": len(public_rows_with_sources),
            "default_visible_verified_rows": len(public_rows_verified),
        },
        "launch_blockers": launch_blockers,
        "program_blockers": blockers,
        "publication_checks": publication_checks,
        "rules": [
            "Maharashtra v1.0 scope only.",
            "No hidden row may be treated as public output.",
            "No admission, branch, salary, package, or job guarantee language.",
            "Every public row must have source URLs and required quality status.",
            "Rows pending verification remain internal until evidence checks pass.",
        ],
    }
