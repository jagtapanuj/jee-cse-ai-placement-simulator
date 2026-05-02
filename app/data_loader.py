from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

from .models import Program, clean_str

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@lru_cache(maxsize=4)
def load_programs(path: str | None = None) -> List[Program]:
    csv_path = Path(path) if path else DATA_DIR / "programs.csv"
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        return [Program.from_row(row) for row in csv.DictReader(f)]


@lru_cache(maxsize=4)
def load_sources(path: str | None = None) -> List[Dict[str, str]]:
    csv_path = Path(path) if path else DATA_DIR / "source_register.csv"
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        return [{k: clean_str(v) for k, v in row.items()} for row in csv.DictReader(f)]


@lru_cache(maxsize=4)
def load_quality_audit(path: str | None = None) -> List[Dict[str, str]]:
    csv_path = Path(path) if path else DATA_DIR / "data_quality_audit.csv"
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        return [{k: clean_str(v) for k, v in row.items()} for row in csv.DictReader(f)]


def get_program(program_key: str) -> Program | None:
    key = program_key.strip()
    for program in load_programs():
        if program.program_key == key:
            return program
    return None
