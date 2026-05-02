-- Maharashtra Simulator API v6 - verified/staged local schema
CREATE TABLE IF NOT EXISTS v6_programs (
    program_key TEXT PRIMARY KEY,
    college TEXT NOT NULL,
    program TEXT NOT NULL,
    route TEXT NOT NULL,
    admission_cutoff_status TEXT,
    admission_seat_type TEXT,
    closing_rank_or_merit NUMERIC,
    closing_score NUMERIC,
    placement_status TEXT,
    placement_confidence NUMERIC,
    placement_score NUMERIC,
    salary_score NUMERIC,
    roi_score_fee_only NUMERIC,
    branch_score NUMERIC,
    internal_job_score_v3 NUMERIC,
    data_quality_status TEXT NOT NULL,
    publish_default BOOLEAN NOT NULL DEFAULT FALSE,
    why_not_ready TEXT,
    source_urls TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS v6_data_quality_audit (
    audit_id SERIAL PRIMARY KEY,
    program_key TEXT REFERENCES v6_programs(program_key),
    publish_default BOOLEAN,
    data_quality_status TEXT,
    issues TEXT,
    required_next_action TEXT,
    source_urls TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
