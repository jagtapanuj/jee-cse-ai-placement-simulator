from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
import math


def clean_str(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none", "null"}:
        return ""
    return text


def parse_float(value: Any) -> Optional[float]:
    text = clean_str(value)
    if not text:
        return None
    try:
        val = float(text)
        if math.isnan(val):
            return None
        return val
    except Exception:
        return None


def parse_int(value: Any) -> Optional[int]:
    val = parse_float(value)
    if val is None:
        return None
    return int(round(val))


def is_yes(value: Any) -> bool:
    return clean_str(value).lower() in {"yes", "y", "true", "1", "publish", "published"}


@dataclass(frozen=True)
class Program:
    program_key: str
    college: str
    program: str
    route: str
    admission_cutoff_status: str
    admission_seat_type: str
    closing_rank_or_merit: Optional[int]
    closing_score: Optional[float]
    placement_status: str
    placement_confidence: Optional[float]
    placement_score: Optional[float]
    salary_score: Optional[float]
    roi_score_fee_only: Optional[float]
    branch_score: Optional[float]
    internal_job_score_v3: Optional[float]
    data_quality_status: str
    publish_default: bool
    why_not_ready: str
    source_urls: str

    @classmethod
    def from_row(cls, row: Dict[str, Any]) -> "Program":
        return cls(
            program_key=clean_str(row.get("program_key")),
            college=clean_str(row.get("college")),
            program=clean_str(row.get("program")),
            route=clean_str(row.get("route")),
            admission_cutoff_status=clean_str(row.get("admission_cutoff_status")),
            admission_seat_type=clean_str(row.get("admission_seat_type")),
            closing_rank_or_merit=parse_int(row.get("closing_rank_or_merit")),
            closing_score=parse_float(row.get("closing_score")),
            placement_status=clean_str(row.get("placement_status")),
            placement_confidence=parse_float(row.get("placement_confidence")),
            placement_score=parse_float(row.get("placement_score")),
            salary_score=parse_float(row.get("salary_score")),
            roi_score_fee_only=parse_float(row.get("roi_score_fee_only")),
            branch_score=parse_float(row.get("branch_score")),
            internal_job_score_v3=parse_float(row.get("internal_job_score_v3")),
            data_quality_status=clean_str(row.get("data_quality_status")),
            publish_default=is_yes(row.get("publish_default")),
            why_not_ready=clean_str(row.get("why_not_ready")),
            source_urls=clean_str(row.get("source_urls")),
        )

    def source_url_list(self) -> List[str]:
        if not self.source_urls:
            return []
        return [u.strip() for u in self.source_urls.split("|") if u.strip()]

    def public_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["publish_default"] = self.publish_default
        data["source_urls"] = self.source_url_list()
        return data
