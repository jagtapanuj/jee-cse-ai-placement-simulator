from __future__ import annotations

APP_NAME = "Maharashtra CSE/AI Job & Placement Simulator"
APP_VERSION = "0.9.0"
TARGET_PRODUCTION_VERSION = "1.0.0"
DATA_VERSION = "mh-2026-dataset-0.9.0"
DATA_SCOPE = "Maharashtra-only CSE/IT/AI/DS"
RELEASE_STAGE = "staging"
DEFAULT_VISIBILITY_RULE = "Only publish_default=yes rows are visible by default."


def version_payload() -> dict:
    return {
        "status": "ok",
        "app_name": APP_NAME,
        "app_version": APP_VERSION,
        "target_production_version": TARGET_PRODUCTION_VERSION,
        "data_version": DATA_VERSION,
        "data_scope": DATA_SCOPE,
        "release_stage": RELEASE_STAGE,
        "default_visibility_rule": DEFAULT_VISIBILITY_RULE,
    }
