from __future__ import annotations

from typing import Any, Dict, List

from .data_loader import get_program, load_program_publication_reviews, load_publication_checks


PASSED_PUBLICATION_STATUS = "passed"


def publication_review(program_key: str) -> Dict[str, Any]:
    program = get_program(program_key)
    if not program:
        raise KeyError(f"Unknown program_key: {program_key}")

    checks = load_publication_checks()
    reviews = [
        review for review in load_program_publication_reviews()
        if review.get("program_key") == program.program_key
    ]
    review_by_check = {review.get("check_key"): review for review in reviews}

    check_results: List[Dict[str, Any]] = []
    pending_or_failed = []

    for check in checks:
        check_key = check.get("check_key", "")
        review = review_by_check.get(check_key)
        status = (review or {}).get("status", "missing")
        passed = status == PASSED_PUBLICATION_STATUS

        row = {
            "check_key": check_key,
            "check_name": check.get("check_name", ""),
            "required_for_v1": check.get("required_for_v1", ""),
            "description": check.get("description", ""),
            "status": status,
            "passed": passed,
            "review_source": (review or {}).get("review_source", ""),
            "reviewed_by": (review or {}).get("reviewed_by", ""),
            "reviewed_at": (review or {}).get("reviewed_at", ""),
            "notes": (review or {}).get("notes", "Missing program publication review row."),
        }
        check_results.append(row)

        if str(check.get("required_for_v1", "")).lower() == "yes" and not passed:
            pending_or_failed.append(check_key)

    required_checks = [
        check for check in checks
        if str(check.get("required_for_v1", "")).lower() == "yes"
    ]

    all_required_checks_passed = len(pending_or_failed) == 0
    can_publish_default = (
        all_required_checks_passed
        and program.data_quality_status == "PILOT_SCORE_READY_VERIFIED"
        and bool(program.source_url_list())
        and program.internal_job_score_v3 is not None
    )

    return {
        "program": program.public_dict(),
        "summary": {
            "required_checks": len(required_checks),
            "passed_required_checks": len(required_checks) - len(pending_or_failed),
            "pending_or_failed_required_checks": len(pending_or_failed),
            "all_required_checks_passed": all_required_checks_passed,
            "can_publish_default": can_publish_default,
        },
        "pending_or_failed_check_keys": pending_or_failed,
        "checks": check_results,
        "rules": [
            "A row can become public only when all required publication checks pass.",
            "Manual review must be complete before publish_default can be yes.",
            "No hidden row should be treated as public output.",
            "No admission, salary, package, branch, or job guarantee language.",
        ],
    }
