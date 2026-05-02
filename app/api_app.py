from __future__ import annotations

from typing import List, Optional

try:
    from fastapi import FastAPI, HTTPException, Query
    from pydantic import BaseModel, Field
except Exception as exc:  # pragma: no cover - useful message when dependency absent
    raise RuntimeError("FastAPI dependencies are not installed. Run: pip install -r requirements.txt") from exc

from .simulator_core import compare as compare_programs
from .simulator_core import data_quality_summary, list_programs, simulate, source_drawer

app = FastAPI(
    title="Maharashtra JEE/CAP CSE-AI Job & Placement Simulator API",
    version="0.8.0",
    description="Pilot API with strict publish_default safety gate. Not a public final college database.",
)


class SimulateRequest(BaseModel):
    rank: Optional[int] = Field(None, description="Candidate rank/merit number. Must match rank_type and route.")
    rank_type: str = Field("UNKNOWN", description="MHT_CET_MERIT, JEE_MAIN_CRL, JEE_MAIN_CATEGORY, or UNKNOWN")
    include_partial: bool = Field(False, description="Internal-only: include rows hidden by default.")
    branch_query: Optional[str] = None
    max_results: int = Field(25, ge=1, le=100)


class CompareRequest(BaseModel):
    program_keys: List[str]
    include_partial: bool = False


@app.get("/health")
def health():
    return {"status": "ok", "data_version": "maharashtra-v6-localapp-v8-patch"}


@app.get("/data-quality")
def data_quality():
    return data_quality_summary()


@app.get("/programs")
def programs(include_partial: bool = Query(False)):
    return {"programs": list_programs(include_partial=include_partial)}


@app.post("/simulate")
def simulate_endpoint(payload: SimulateRequest):
    return simulate(
        rank=payload.rank,
        rank_type=payload.rank_type,
        include_partial=payload.include_partial,
        branch_query=payload.branch_query,
        max_results=payload.max_results,
    )


@app.post("/compare")
def compare_endpoint(payload: CompareRequest):
    return {"programs": compare_programs(payload.program_keys, include_partial=payload.include_partial)}


@app.get("/sources/{program_key}")
def sources(program_key: str):
    try:
        return source_drawer(program_key)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
