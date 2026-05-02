from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Any, Dict, Iterable, List, Optional

from .data_loader import get_program, load_programs, load_quality_audit, load_sources
from .models import Program

VALID_RANK_TYPES = {"MHT_CET_MERIT", "JEE_MAIN_CRL", "JEE_MAIN_CATEGORY", "UNKNOWN"}


def admission_bucket(user_rank: Optional[int], closing_rank: Optional[int]) -> str:
    """Return historical feasibility bucket. Lower rank/merit number is better.

    This bucket is only meaningful when user_rank and closing_rank are from the same route/rank type.
    """
    if user_rank is None or closing_rank is None or closing_rank <= 0:
        return "NEEDS_VERIFIED_CUTOFF"
    ratio = user_rank / closing_rank
    if ratio <= 0.80:
        return "SAFE_HISTORICAL"
    if ratio <= 1.05:
        return "LIKELY_TARGET"
    if ratio <= 1.25:
        return "BORDERLINE"
    if ratio <= 1.50:
        return "REACH"
    return "UNLIKELY"


def route_warning(program: Program, rank_type: str) -> Optional[str]:
    route = program.route.lower()
    if "mht" in route or "cap" in route:
        if rank_type not in {"MHT_CET_MERIT", "UNKNOWN"}:
            return "This row is Maharashtra CAP/MHT-CET oriented. Do not compare it directly with JEE Main AIR unless the source row is an AI/JEE seat and verified."
    if "josaa" in route or "iiit" in route:
        if rank_type not in {"JEE_MAIN_CRL", "JEE_MAIN_CATEGORY", "UNKNOWN"}:
            return "This row is JoSAA/JEE oriented. Do not compare it directly with MHT-CET merit rank."
    return None


def visibility_filter(programs: Iterable[Program], include_partial: bool = False) -> List[Program]:
    if include_partial:
        return list(programs)
    return [p for p in programs if p.publish_default]


def list_programs(include_partial: bool = False) -> List[Dict[str, Any]]:
    return [p.public_dict() for p in visibility_filter(load_programs(), include_partial)]


def data_quality_summary() -> Dict[str, Any]:
    """Return a data-readiness summary for the local pilot.

    This endpoint is deliberately read-only. It does not promote any hidden row.
    It is meant to help the project owner/admin see why rows are blocked.
    """
    programs = load_programs()
    sources = load_sources()
    audit = load_quality_audit()

    status_counts = Counter(p.data_quality_status or "UNKNOWN" for p in programs)
    route_counts = Counter(p.route or "UNKNOWN_ROUTE" for p in programs)
    placement_status_counts = Counter(p.placement_status or "UNKNOWN_PLACEMENT_STATUS" for p in programs)

    hidden_rows = [p for p in programs if not p.publish_default]
    default_rows = [p for p in programs if p.publish_default]

    missing_cutoff = [
        p for p in programs
        if "no_verified_cutoff" in (p.admission_cutoff_status or "").lower()
        or "staged" in (p.admission_cutoff_status or "").lower()
    ]
    missing_or_partial_placement = [
        p for p in programs if p.data_quality_status != "PILOT_SCORE_READY_VERIFIED"
    ]
    missing_sources = [p for p in programs if not p.source_url_list()]

    hidden_blockers = []
    for p in hidden_rows:
        hidden_blockers.append({
            "program_key": p.program_key,
            "college": p.college,
            "program": p.program,
            "route": p.route,
            "data_quality_status": p.data_quality_status,
            "placement_status": p.placement_status,
            "admission_cutoff_status": p.admission_cutoff_status,
            "why_not_ready": p.why_not_ready,
            "source_count": len(p.source_url_list()),
        })

    return {
        "data_version": "maharashtra-v6-localapp-v8-patch",
        "summary": {
            "total_program_rows": len(programs),
            "default_visible_rows": len(default_rows),
            "hidden_pending_verification_rows": len(hidden_rows),
            "source_register_rows": len(sources),
            "quality_audit_rows": len(audit),
            "rows_missing_or_staged_cutoff": len(missing_cutoff),
            "rows_partial_or_not_public": len(missing_or_partial_placement),
            "rows_missing_source_urls": len(missing_sources),
        },
        "status_counts": dict(status_counts),
        "route_counts": dict(route_counts),
        "placement_status_counts": dict(placement_status_counts),
        "hidden_blockers": hidden_blockers,
        "safety_gate": "Only publish_default=yes rows are visible by default. Hidden rows must remain internal until source, cutoff, denominator, fee, confidence, and last-verified checks pass.",
    }


def source_drawer(program_key: str) -> Dict[str, Any]:
    program = get_program(program_key)
    if not program:
        raise KeyError(f"Unknown program_key: {program_key}")
    college_sources = [s for s in load_sources() if s.get("college") == program.college]
    audit = [a for a in load_quality_audit() if a.get("program_key") == program.program_key]
    return {
        "program": program.public_dict(),
        "program_source_urls": program.source_url_list(),
        "college_sources": college_sources,
        "quality_audit": audit,
        "manual_verification_required": program.data_quality_status != "PILOT_SCORE_READY_VERIFIED",
        "warning": "Use as public data only after row-level source, year, branch/program, denominator, confidence, and last-verified checks pass.",
    }


def compare(program_keys: List[str], include_partial: bool = False) -> List[Dict[str, Any]]:
    allowed_keys = {p.program_key for p in visibility_filter(load_programs(), include_partial)}
    results = []
    for key in program_keys:
        program = get_program(key)
        if not program:
            continue
        if key not in allowed_keys:
            continue
        results.append(program.public_dict())
    results.sort(
        key=lambda x: (
            x.get("internal_job_score_v3") is not None,
            x.get("internal_job_score_v3") or 0,
        ),
        reverse=True,
    )
    return results


def simulate(
    rank: Optional[int] = None,
    rank_type: str = "UNKNOWN",
    include_partial: bool = False,
    branch_query: Optional[str] = None,
    max_results: int = 25,
) -> Dict[str, Any]:
    if rank_type not in VALID_RANK_TYPES:
        raise ValueError(f"rank_type must be one of {sorted(VALID_RANK_TYPES)}")
    programs = visibility_filter(load_programs(), include_partial)
    if branch_query:
        bq = branch_query.strip().lower()
        programs = [p for p in programs if bq in p.program.lower()]

    rows: List[Dict[str, Any]] = []
    for p in programs:
        bucket = admission_bucket(rank, p.closing_rank_or_merit)
        warnings = []
        rw = route_warning(p, rank_type)
        if rw:
            warnings.append(rw)
        if not p.publish_default:
            warnings.append("Hidden by default: not public score-ready yet.")
        if p.data_quality_status != "PILOT_SCORE_READY_VERIFIED":
            warnings.append(f"Data quality status: {p.data_quality_status}.")
        if p.why_not_ready:
            warnings.append(p.why_not_ready)
        if not p.source_url_list():
            warnings.append("No source URL attached. Do not publish.")

        rows.append({
            "program_key": p.program_key,
            "college": p.college,
            "program": p.program,
            "route": p.route,
            "admission_bucket": bucket,
            "closing_rank_or_merit": p.closing_rank_or_merit,
            "closing_score": p.closing_score,
            "job_strength_score": p.internal_job_score_v3,
            "placement_confidence": p.placement_confidence,
            "placement_status": p.placement_status,
            "data_quality_status": p.data_quality_status,
            "publish_default": p.publish_default,
            "warnings": warnings,
            "source_count": len(p.source_url_list()),
        })

    rows.sort(
        key=lambda x: (
            x.get("publish_default", False),
            x.get("job_strength_score") or 0,
        ),
        reverse=True,
    )
    return {
        "data_version": "maharashtra-v6-localapp-v8-patch",
        "input": {
            "rank": rank,
            "rank_type": rank_type,
            "include_partial": include_partial,
            "branch_query": branch_query,
        },
        "safety_gate": "Default output includes only publish_default=yes rows. Use include_partial=true only for internal testing.",
        "results": rows[:max_results],
        "counts": {
            "total_loaded": len(load_programs()),
            "visible_returned": min(len(rows), max_results),
            "default_publishable_total": len([p for p in load_programs() if p.publish_default]),
            "hidden_pending_verification": len([p for p in load_programs() if not p.publish_default]),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Maharashtra simulator locally.")
    parser.add_argument("--rank", type=int, default=None, help="Candidate rank/merit number. Must match rank_type/route.")
    parser.add_argument("--rank-type", default="UNKNOWN", choices=sorted(VALID_RANK_TYPES))
    parser.add_argument("--include-partial", action="store_true", help="Show rows hidden by default. Internal testing only.")
    parser.add_argument("--branch", default=None)
    parser.add_argument("--max-results", type=int, default=25)
    parser.add_argument("--data-quality", action="store_true", help="Print data-quality summary instead of simulation results.")
    args = parser.parse_args()

    if args.data_quality:
        print(json.dumps(data_quality_summary(), indent=2))
    else:
        print(json.dumps(
            simulate(args.rank, args.rank_type, args.include_partial, args.branch, args.max_results),
            indent=2,
        ))


if __name__ == "__main__":
    main()
